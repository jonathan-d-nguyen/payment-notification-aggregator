<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/jonathan-d-nguyen/payment-notification-aggregator">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<h3 align="center">Soccer Payment Notification Aggregator</h3>

  <p align="center">
    An automated system to track and verify soccer meetup payments through email notifications from Zelle/Venmo, storing payment data in DynamoDB and syncing with iOS Reminders for easy participant check-off on Apple Watch.
    <br />
    <a href="https://github.com/jonathan-d-nguyen/payment-notification-aggregator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jonathan-d-nguyen/payment-notification-aggregator">View Demo</a>
    ·
    <a href="https://github.com/jonathan-d-nguyen/payment-notification-aggregator/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/jonathan-d-nguyen/payment-notification-aggregator/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#architecture">Architecture</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#multi-cloud-architecture">Multi-Cloud Architecture</a></li>
    <li><a href="#implementation-plan">Implementation Plan</a></li>
    <li><a href="#security-and-compliance">Security and Compliance</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://www.jdnguyen.net) -->

A serverless solution for automating payment tracking for soccer meetups. The system processes payment notifications from Zelle and Venmo via AWS SES, parses the information using Lambda functions, stores the data in DynamoDB, and syncs with iOS Reminders for easy participant management.

### Architecture

- **Email Processing**: AWS SES receives payment notifications from Zelle/Venmo
- **Data Extraction**: Python Lambda function parses email content for payment details
- **Data Storage**: DynamoDB stores payment records and participant information
- **Task Management**: Integration with iOS Reminders for participant check-off
- **Infrastructure**: Terraform for AWS resource provisioning and management

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
- ![DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

- AWS Account with appropriate permissions
- Python 3.8+
- Terraform
- AWS CLI configured
- iOS device for Reminders integration

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation

1. Clone the repository

   ```sh
   git clone https://github.com/jonathan-d-nguyen/payment-notification-aggregator.git
   ```

2. Install Python dependencies

   ```sh
   pip install -r requirements.txt
   ```

3. Configure AWS credentials

   ```sh
   aws configure
   ```

4. Set up environment variables in `.env`

   ```
   AWS_REGION=your_region
   SES_EMAIL=your_ses_verified_email
   REMINDER_LIST_ID=your_ios_reminder_list_id
   ```

5. Initialize Terraform
   ```sh
   cd terraform
   terraform init
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Current functionality:

- Email parsing for Zelle/Venmo notifications via AWS SES
- Python scripts for payment information extraction

In progress:

- DynamoDB integration
- iOS Reminders sync
- Terraform infrastructure setup

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Multi-Cloud Architecture

### Infrastructure Components

- **Email Ingestion**

  - Primary: AWS SES
  - Alternatives: Azure Communication Services, GCP Cloud Tasks
  - Multi-region failover capability

- **Processing Layer**

  - AWS Lambda (primary)
  - Azure Functions (secondary)
  - GCP Cloud Functions (tertiary)
  - Load balancing across cloud providers

- **Storage Strategy**

  - Hot Data: DynamoDB with global tables
  - Cold Storage: Multi-cloud blob storage (S3/Azure Blob/GCP Storage)
  - Automated archival policies

- **Event Processing**

  - AWS EventBridge for primary orchestration
  - Cross-cloud event synchronization
  - Dead letter queues for failed events

- **Secrets Management**
  - HashiCorp Vault as central secret store
  - Cloud KMS integration for key management
  - Automatic secret rotation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Design Principles

1. **Cloud Agnostic Core**

   - Provider-neutral business logic
   - Abstracted cloud services
   - Portable configurations

2. **Event-Driven Architecture**

   - Asynchronous processing
   - Loose coupling
   - Scalable message handling

3. **Security-First Approach**

   - Zero-trust architecture
   - Encryption everywhere
   - Least privilege access

4. **Comprehensive Monitoring**

   - Cross-cloud metrics aggregation
   - Centralized logging
   - Real-time alerting

5. **Cost Optimization**
   - Dynamic resource allocation
   - Multi-cloud cost analysis
   - Automated scaling policies
   <p align="right">(<a href="#readme-top">back to top</a>)</p>

## Implementation Plan

### 1. Infrastructure Setup

```
# payment-notification-aggregator/
├── infrastructure
│   └── cloudformation
│       └── templates
│           └── template.yaml
├── src
│   ├── extractors
│   │   ├── venmo_extractor.py
│   │   └── zelle_extractor.py
│   ├── processors
│   │   ├── email_processor.py
│   │   ├── venmo_processor.py
│   │   └── zelle_processor.py
│   └── utils
│       └── output_formatter.py
├── .gitignore
├── Dockerfile
├── main.py
├── main.tf
├── README.md
└── requirements.txt
```

<details>
<summary>
Prospective Infrastructure (click to expand)
</summary>

```
# payment-notification-aggregator/
│
├── terraform/
│   ├── modules/
│   │   ├── core/                 # Cloud-agnostic modules
│   │   │   ├── vault/
│   │   │   │   ├── main.tf
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   └── monitoring/      # Shared monitoring setup
│   │   │
│   │   ├── aws/                 # AWS-specific resources
│   │   │   ├── ses/
│   │   │   │   ├── main.tf      # Email ingestion setup
│   │   │   │   ├── variables.tf
│   │   │   │   └── outputs.tf
│   │   │   ├── lambda/
│   │   │   └── dynamodb/
│   │   │
│   │   ├── azure/               # Future Azure implementation
│   │   │   ├── logic_apps/
│   │   │   ├── functions/
│   │   │   └── cosmos_db/
│   │   │
│   │   └── gcp/                 # Future GCP implementation
│   │       ├── cloud_functions/
│   │       ├── pub_sub/
│   │       └── firestore/
│   │
│   └── environments/
│       ├── dev/
│       │   ├── main.tf
│       │   ├── variables.tf
│       │   ├── outputs.tf
│       │   └── backend.tf
│       └── prod/
└── └── [same as dev]
│
├── src/
│   ├── core/
│   │   ├── interfaces/
│   │   │   ├── email_processor.py    # Abstract base classes
│   │   │   └── storage.py
│   │   │
│   │   └── models/
│   │       ├── transaction.py         # Data models
│   │       └── reminder.py
│   │
│   ├── processors/
│   │   ├── parsers/
│   │   │   ├── venmo_parser.py       # Venmo-specific parsing
│   │   │   └── zelle_parser.py       # Zelle-specific parsing
│   │   │
│   │   └── filters/
│   │       └── incoming_filter.py     # Filter for received money only
│   │
│   ├── services/
│   │   ├── vault_service.py          # HashiCorp Vault integration
│   │   ├── email_service.py          # Email processing service
│   │   └── reminder_service.py       # iOS Reminders integration
│   │
│   └── utils/
│       ├── config.py
│       ├── logging.py
│       └── error_handling.py
│
├── docker/
│   ├── Dockerfile               # Multi-stage build
│   ├── docker-compose.yml       # Local development setup
│   └── vault/
│       ├── config.hcl          # Vault configuration
│       └── policies/
│           └── app-policy.hcl  # Access policies
│
├── tests/
│   ├── unit/
│   │   ├── test_parsers.py
│   │   ├── test_filters.py
│   │   └── test_services.py
│   │
│   ├── integration/
│   │   ├── test_email_flow.py
│   │   └── test_reminder_creation.py
│   │
│   └── fixtures/
│       ├── sample_emails/      # Test email templates
│       │   ├── venmo/
│       │   └── zelle/
│       └── expected_outputs/   # Expected parsing results
│
├── scripts/
│   ├── deploy.sh              # Deployment automation
│   ├── vault-setup.sh         # Vault initialization
│   └── local-setup.sh         # Development environment setup
│
├── docs/
│   ├── architecture.md        # System design documentation
│   ├── setup.md              # Setup instructions
│   ├── deployment.md         # Deployment guide
│   └── cloud-specific/       # Provider-specific details
│       ├── aws.md
│       ├── azure.md
│       └── gcp.md
│
├── .github/
│   └── workflows/
│       ├── test.yml              # Unit and integration tests
│       ├── lint.yml              # Code quality checks
│       └── deploy.yml            # Multi-cloud deployment pipeline
│
├── .gitignore
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Python project configuration
└── README.md               # Project overview and quickstart
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 2. Processing Pipeline

1. **Email Reception**

   - Multi-provider email ingestion
   - Unified filtering rules
   - Cross-cloud storage replication

2. **Processing Function**

   - Cloud-agnostic business logic
   - Cross-cloud message routing
   - Unified error handling

3. **Data Storage**

   - Multi-region data replication
   - Cross-cloud backup strategy
   - Automated data lifecycle

4. **Reminder Integration**
   - Resilient webhook system
   - Cross-platform compatibility
   - Failure recovery mechanism

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Security and Compliance

### Authentication & Authorization

- OAuth/OIDC integration
- Cross-cloud IAM strategy
- Zero-trust network design

### Monitoring & Observability

- Unified logging strategy
- Cross-cloud metrics
- Centralized alerting

### Error Handling

- Global retry policies
- Cross-cloud circuit breakers
- Unified error reporting

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [x] AWS SES Configuration
- [x] Python Email Parser Development
- [ ] Multi-Cloud Infrastructure Setup
- [ ] Cross-Cloud Event Processing
- [ ] Global Data Replication
- [ ] Security Hardening
- [ ] Monitoring Implementation
- [ ] Cost Optimization
- [ ] Compliance Framework
- [ ] Disaster Recovery Testing

See the [open issues](https://github.com/jonathan-d-nguyen/payment-notification-aggregator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Jonathan Nguyen - [@twitter_handle](https://twitter.com/twitter_handle) - jonathan@jdnguyen.tech

Project Link: [https://github.com/jonathan-d-nguyen/payment-notification-aggregator](https://github.com/jonathan-d-nguyen/payment-notification-aggregator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/jonathan-d-nguyen/payment-notification-aggregator.svg?style=for-the-badge
[contributors-url]: https://github.com/jonathan-d-nguyen/payment-notification-aggregator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jonathan-d-nguyen/payment-notification-aggregator.svg?style=for-the-badge
[forks-url]: https://github.com/jonathan-d-nguyen/payment-notification-aggregator/network/members
[stars-shield]: https://img.shields.io/github/stars/jonathan-d-nguyen/payment-notification-aggregator.svg?style=for-the-badge
[stars-url]: https://github.com/jonathan-d-nguyen/payment-notification-aggregator/stargazers
[issues-shield]: https://img.shields.io/github/issues/jonathan-d-nguyen/payment-notification-aggregator.svg?style=for-the-badge
[issues-url]: https://github.com/jonathan-d-nguyen/payment-notification-aggregator/issues
[license-shield]: https://img.shields.io/github/license/jonathan-d-nguyen/payment-notification-aggregator.svg?style=for-the-badge
[license-url]: https://github.com/jonathan-d-nguyen/payment-notification-aggregator/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/JonathanDanhNguyen
[product-screenshot]: images/screenshot.png
