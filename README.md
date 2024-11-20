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

## Roadmap

- [x] AWS SES Configuration
- [x] Python Email Parser Development
- [ ] DynamoDB Table Creation and Integration
- [ ] iOS Reminders Integration
- [ ] Terraform Infrastructure Setup
- [ ] Monitoring and Alerting
- [ ] User Interface for Payment Status

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
[linkedin-url]: https://linkedin.com/in/JonathanDanhNguyene
[product-screenshot]: images/screenshot.png
