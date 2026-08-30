# DynamoDB Evidence - Bug Report Tickets

## Account Information
- **Account ID:** 741147167620
- **Account Name:** c0w2152638t1617123650
- **Federated User:** voclabs/user5323274=ce604d6e-9c2d-4c02-a6fc-8c38946c20b8
- **Region:** us-east-1
- **Date:** August 30, 2026

## Table Information

| Attribute | Value |
|-----------|-------|
| **Table Name** | bug-report-tool-stack-bug-reports |
| **Region** | us-east-1 |
| **Status** | ACTIVE |
| **Billing Mode** | PAY_PER_REQUEST |

---

## ACTUAL TICKETS CREATED BY THE CHATBOT

### Ticket 1 (Complete - All 3 Fields Populated)
| Field | Value |
|-------|-------|
| **ticketId** | 2e496443-e042-465e-85c0-406e5b14e4cc |
| **createdAt** | 2026-08-28T04:50:41.106555+00:00 |
| **description** | The checkout page crashes every time I click the Pay button. |
| **stepsToReproduce** | 1. Add an item to the cart. 2. Go to checkout. 3. Click Pay. |
| **environment** | Chrome 120 on Windows 11 |
| **status** | OPEN |

### Ticket 2 (Complete - All 3 Fields Populated)
| Field | Value |
|-------|-------|
| **ticketId** | 99fbc13a-63d8-4ce8-b0a0-9db485c44c65 |
| **createdAt** | 2026-08-28T06:15:52.781298+00:00 |
| **description** | The checkout page crashes when I click the Pay button |
| **stepsToReproduce** | 1. Add an item to the cart. 2. Go to checkout. 3. Click Pay. |
| **environment** | Chrome 120 on macOS Sonoma |
| **status** | OPEN |

### Ticket 3 (Complete - All 3 Fields Populated)
| Field | Value |
|-------|-------|
| **ticketId** | f0316677-a34e-4a82-9e53-537f866934e3 |
| **createdAt** | 2026-08-28T03:49:12.613239+00:00 |
| **description** | Test bug: checkout button fails |
| **stepsToReproduce** | 1. Add item. 2. Open checkout. 3. Click Pay. |
| **environment** | Chrome 120 on Windows 11 |
| **status** | OPEN |

### Ticket 4 (Complete - All 3 Fields Populated)
| Field | Value |
|-------|-------|
| **ticketId** | a4a79d11-983a-418a-9d2d-c2dc946ea2ac |
| **createdAt** | 2026-08-28T13:04:27.262338+00:00 |
| **description** | The checkout page crashes when I click the Pay button |
| **stepsToReproduce** | 1. Add an item to the cart. 2. Go to checkout. 3. Click Pay. |
| **environment** | Chrome 120 on macOS Sonoma |
| **status** | OPEN |

### Ticket 5 (Complete - All 3 Fields Populated)
| Field | Value |
|-------|-------|
| **ticketId** | 8be9f1f8-47c8-405b-b7cd-562eea577f01 |
| **createdAt** | 2026-08-28T06:13:39.141939+00:00 |
| **description** | The checkout page crashes when I click the Pay button |
| **stepsToReproduce** | 1. Add an item to the cart. 2. Go to checkout. 3. Click Pay. |
| **environment** | Chrome 120 on macOS Sonoma |
| **status** | OPEN |

---

## ISSUES IDENTIFIED FROM DYNAMODB DATA

### Problematic Tickets (Missing Environment Field)

| ticketId | Issue | environment value |
|----------|-------|-------------------|
| f19ce928-325b-4cb4-bc74-088f8aea88b2 | Missing environment | "Not provided" |
| db7c7b95-d8cb-4929-8007-b8dac0f4ab2a | Missing environment | "Unknown" |
| 32e3a1b2-bc03-44ff-93b2-33ba64a7383a | Missing environment | "User's browser, operating system, and device" |
| febd468f-6cb9-4c6b-a251-d48d474cb82c | Missing environment | "Please provide your device, operating system, and browser information." |
| bfebb3db-1103-4ace-9464-5fabee5b3ad3 | Missing environment | "Please provide your device, operating system, and browser information." |
| ce206c01-37fb-4d6d-bb9e-221156e2c4c5 | Missing environment | "Please provide your device, operating system, and browser information." |

**Important Note:** These tickets show the chatbot was calling the tool WITHOUT collecting the environment field, which violates the requirement to collect all three fields before calling the tool.

---

## AWS CLI Verification Command

```bash
aws dynamodb scan \
    --table-name bug-report-tool-stack-bug-reports \
    --region us-east-1 \
    --profile default