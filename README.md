<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
![Language][language-shield]
![Repo Size][reposize-shield]
![Last Commit][last-commit-shield]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Medium][medium-shield]][medium-url]
[![Twitter][twitter-shield]][twitter-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/trujillo9616/BreakableToy">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Ledgertruji</h3>

  <p align="center">
    A simple Ledger CLI implementation in Python.
    <br />
    <a href="https://github.com/trujillo9616/BreakableToy"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/trujillo9616/BreakableToy">View Demo</a>
    ·
    <a href="https://github.com/trujillo9616/BreakableToy/issues">Report Bug</a>
    ·
    <a href="https://github.com/trujillo9616/BreakableToy/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)


### Built With

* [Python](https://www.python.org/)
* [Argparse](https://docs.python.org/3/library/argparse.html)
* [Numpy](https://numpy.org/)
* [Tabulate](https://pypi.org/project/tabulate/)
* [Colored](https://pypi.org/project/colored/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Prior to installing and downloading the files you will need to have Python installed. You can find the installation instructions [here](https://www.python.org/downloads/). Or run the following command to install Python.
* npm
  ```sh
  brew install python
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/trujillo9616/BreakableToy.git
   ```
2. Install packages
   ```sh
   pip3 install requirements.txt
   ```
3. Run the project
   ```sh
   python3 ledgertruji.py --help
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This small implementation of the Ledger CLI in Python supports the following commands and flags:

REQUIRED FLAG:
- File: Read FILE as a ledger file.
    -f --file {filename}


REQUIRED COMMAND (Only enter one of the following):
- Print: The print command prints out ledger transactions in a textual format that can be parsed by Ledger. They will be properly formatted, and output in the most economic form possible.
    print

- Register: The register command displays all the postings occurring in a single account, line by line. The output from register is very close to what a typical checkbook, or single-account ledger, would look like. It also shows a running balance. The final running balance of any register should always be the same as the current balance of that account.
    reg register

- Balance: The balance command reports the current balance of all accounts. If an account contains multiple types of commodities, each commodity’s total is reported separately.
    bal balance


OPTIONAL FLAGS:
- File: Read FILE as a ledger file.
    -f --file {filename}

- Sort: Sort the register or print report based on the date the postings were made.
    -s --sort {d}

- Price-DB: Use FILE for retrieving stored commodity prices. Display values in terms of the given currency or commodity. The specified currency or commodity must be in the price-db.
    -p --price-db {filename currency/commodity}



<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [] Colored Results (negative numbers in red!)
- [] Filter results based on a regex input
- [] Multiple reports

See the [open issues](https://github.com/trujillo9616/BreakableToy/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Adrian Trujillo - [@trujillo9616](https://twitter.com/trujillo9616)com

Project Link: [https://github.com/trujillo9616/BreakableToy](https://github.com/trujillo9616/BreakableToy)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Staff memebers and mentors for their guidance and support
* Jorge Garcia for his support and providing me resources that allowed me to develop the project

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/trujillo9616/breakabletoy?style=plastic
[contributors-url]: https://github.com/trujillo9616/BreakableToy/graphs/contributors

[language-shield]: https://img.shields.io/github/languages/top/trujillo9616/breakabletoy?style=plastic

[reposize-shield]: https://img.shields.io/github/repo-size/trujillo9616/breakabletoy?style=plastic

[last-commit-shield]: https://img.shields.io/github/last-commit/trujillo9616/breakabletoy?style=plastic

[license-shield]: https://img.shields.io/github/license/trujillo9616/breakabletoy?style=plastic
[license-url]: https://github.com/trujillo9616/BreakableToy/blob/main/LICENSE


[twitter-shield]: https://img.shields.io/twitter/follow/trujillo9616?style=social
[twitter-url]: https://twitter.com/trujillo9616

[linkedin-shield]: https://img.shields.io/badge/LinkedIn-Connect-blue?style=social&logo=linkedin
[linkedin-url]: https://www.linkedin.com/in/adrian-trujillo96/

[medium-shield]: https://img.shields.io/badge/Medium-Connect-black?style=social&logo=medium
[medium-url]: https://medium.com/@adrian.td96

