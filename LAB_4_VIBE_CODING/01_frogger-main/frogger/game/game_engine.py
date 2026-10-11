
"""
GameEngine: owns the frog and all vehicles.
Includes collision detection, lives, score, countdown timer,
respawning, Game Over, and restart.
"""

import random
import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GRID_ROWS, GOAL_ROW, ROAD_ROWS, START_ROW,
    CELL_SIZE, WIDTH, HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]

GOAL_POINTS = 10
ATTEMPT_TIME_MS = 30_000
GOAL_MESSAGE_DURATION = 1500
COLLISION_COOLDOWN_MS = 1000


class GameEngine:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.invulnerable_until = 0
        self.goal_message_until = 0
        self.attempt_started_at = pygame.time.get_ticks()
        self._build_entities()

    def _build_entities(self):
        start_col = GRID_COLS // 2

        self.frog = Frog(
            col=start_col,
            row=START_ROW,
            start_col=start_col,
            start_row=START_ROW,
            cols=GRID_COLS,
            start_row_limit=START_ROW,
        )

        frog_x_range = (
            start_col * CELL_SIZE,
            start_col * CELL_SIZE + CELL_SIZE,
        )

        self.vehicles = []

        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70
            spacing = 300
            count = 2

            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True

                for n in range(count):
                    offset = phase + n * spacing
                    x = (
                        offset
                        if speed > 0
                        else WIDTH - offset - vehicle_width
                    )
                    positions.append(x)

                    if not (
                        x + vehicle_width <= frog_x_range[0]
                        or x >= frog_x_range[1]
                    ):
                        safe = False

                if safe:
                    break

            for x in positions:
                self.vehicles.append(
                    Vehicle(
                        x=x,
                        row=row,
                        width=vehicle_width,
                        height=CELL_SIZE - 8,
                        speed=speed,
                    )
                )

    def _reset_attempt_timer(self, current_time=None):
        """Start a fresh 30-second attempt."""
        if current_time is None:
            current_time = pygame.time.get_ticks()

        self.attempt_started_at = current_time

    def _finish_attempt(self, current_time):
        """Respawn after a failed attempt and deduct exactly one life."""
        self.lives -= 1
        self.frog.reset()
        self._reset_attempt_timer(current_time)

        # Prevent the same collision from immediately costing another life.
        self.invulnerable_until = (
            current_time + COLLISION_COOLDOWN_MS
        )

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.lives = 3
            self.score = 0
            self.game_over = False
            self.invulnerable_until = 0
            self.goal_message_until = 0
            self._build_entities()
            self._reset_attempt_timer()
            return

        if self.game_over:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self):
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()

        for vehicle in self.vehicles:
            vehicle.update(road_width_px=WIDTH)

        # 1. Handle vehicle collision.
        if (
            current_time >= self.invulnerable_until
            and check_collision(self.frog, self.vehicles)
        ):
            self._finish_attempt(current_time)
            return

        # 2. Handle timeout. This branch runs only once per attempt
        # because _finish_attempt resets the timer and frog.
        elapsed = current_time - self.attempt_started_at

        if elapsed >= ATTEMPT_TIME_MS:
            self._finish_attempt(current_time)
            return

        # 3. Handle successful goal.
        if self.frog.row == GOAL_ROW:
            self.score += GOAL_POINTS
            self.goal_message_until = (
                current_time + GOAL_MESSAGE_DURATION
            )
            self.frog.reset()
            self._reset_attempt_timer(current_time)

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.frog, self.vehicles)

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.attempt_started_at
        remaining_ms = max(0, ATTEMPT_TIME_MS - elapsed)

        # Round up so the display starts at 30 and reaches 0 at timeout.
        seconds_remaining = (
            remaining_ms + 999
        ) // 1000

        renderer.draw_text(
            surface, font, f"Lives: {self.lives}", (10, 10)
        )
        renderer.draw_text(
            surface, font, f"Score: {self.score}", (150, 10)
        )
        renderer.draw_text(
            surface, font,
            f"Time: {seconds_remaining}s",
            (270, 10),
        )
        renderer.draw_text(
            surface, font,
            "Arrow keys to move. R to restart.",
            (10, HEIGHT - 24),
        )

        if self.game_over:
            renderer.draw_banner(
                surface, font, "GAME OVER - Press R to restart"
            )
        elif current_time < self.goal_message_until:
            renderer.draw_banner(
                surface, font,
                f"GOAL REACHED! +{GOAL_POINTS} points"
            )
