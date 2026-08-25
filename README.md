# Smart Lab Equipment & Slot Reservation Portal

## Lab 1 — Requirements Engineering & UML Use-Case Modelling

### 1. Problem Statement

**Smart Lab Equipment & Slot Reservation Portal**

The system is designed to manage the scheduling and reservation of laboratory equipment such as oscilloscopes, logic analyzers, and FPGA development boards.

The portal is intended to prevent double-booking of equipment, verify equipment calibration status, and enforce late-return disciplinary rules.

### 2. Actors

The target stakeholders/actors identified in the problem statement are:

* **Student** — Uses the portal to view equipment availability and reserve laboratory equipment.
* **Lab Technician** — Manages laboratory equipment and calibration-related information.

### 3. Requirements Engineering

The Requirements Engineering section contains:

* **5 Functional Requirements (FR-001 to FR-005)**
* **2 Non-Functional Requirements (NFR-001 and NFR-002)**

Each requirement includes:

* Requirement ID
* Type
* Description
* Priority
* Acceptance Criteria
* Rationale

The requirements were derived from the given problem statement and cover equipment reservation, calibration verification, double-booking prevention, equipment returns, equipment management, performance, and authentication/security.

### 4. UML Use-Case Model

The UML Use-Case Diagram represents the interaction between the system and its actors.

The five functional use cases represented in the diagram are:

1. **UC-01 — View Equipment Availability**
2. **UC-02 — Reserve Equipment Slot**
3. **UC-03 — Verify Equipment Calibration**
4. **UC-04 — Handle Equipment Return & Late Return**
5. **UC-05 — Manage Equipment & Calibration Status**

The diagram also represents the required UML relationships such as `«include»` and `«extend»`.

### 5. Use-Case Flow

The detailed Use-Case Flow is provided for:

**UC-02 — Reserve Equipment Slot**

The flow contains:

* Preconditions
* Main Success Scenario
* Postconditions
* Alternate Flows

The alternate flows cover situations such as an unavailable equipment/slot and invalid equipment calibration.

### 6. Repository Contents

| File                                       | Description                                         |
| ------------------------------------------ | --------------------------------------------------- |
| `README.md`                                | Overview of the Lab-1 work and repository contents  |
| `Problem_Statement.pdf`                    | Problem statement provided for the lab              |
| `Requirements_Table.xlsx`                  | Five functional and two non-functional requirements |
| `UML_Use_Case_Diagram.pdf`                 | UML Use-Case Diagram                                |
| `Use_Case_Flow_Reserve_Equipment_Slot.pdf` | Use-Case Flow for UC-02                             |

### 7. Course Information

**Lab:** Lab 1 — Requirements Engineering & UML Use-Case Modelling
**Problem:** Smart Lab Equipment & Slot Reservation Portal
**Student:** Shantheri Shenoy
**Repository:** LAB_1_Activity_Shantheri_Shenoy_PES1UG24CS428
