<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Fourgoblin/documentAnalyzer">
  </a>

<h3 align="center">Document Analysis Tool</h3>

  <p align="center">
    The goal of this project is to create a program that can accurately segment an image of a document. The program will provide coordinates of the found content segements in JSON format, with each segment seperated by whitespace within the document being analyzed.
    <br />
    <a href="https://github.com/Fourgoblin/documentAnalyzer"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Fourgoblin/documentAnalyzer">View Demo</a>
    &middot;
    <a href="https://github.com/Fourgoblin/documentAnalyzer/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Fourgoblin/documentAnalyzer/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is being developed for OpenText by CS499 students at the University of Kentucky.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

For quickest setup simply download the executable from


### Prerequisites

* Tesseract OCR engine (ensure this is installed to C:\Program Files or change the filepath in ImageScanner.py)
  ```sh
  https://github.com/UB-Mannheim/tesseract/wiki
  ```
* Flask
  ```sh
  pip install Flask
  ```
* Tesseract
  ```sh
  pip install pytesseract
  ```
* NumPy
  ```sh
  pip install numpy
  ```
* OpenCV
  ```sh
  pip install opencv-python
  ```
* pyzbar
  ```sh
  pip install pyzbar
  ```
* pdf2image
  ```sh
  pip install pdf2image
  ```

<!-- USAGE EXAMPLES -->
## Usage

The application currently handles most common types of image files. PDF handling is still in development. To use the tool upload a file and use the threshold sliders to adjust to the desired sections. Click and drag the adjustable boxes if any sections need to be adjusted. A JSON file containing document section data will be placed in an "output" directory.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Landon Kuerzi - email, Andrew Mortimer - email, Sharan Ravula - email, Jovani Rivas - email, Mason Zande - masonzande@live.com

Project Link: [https://github.com/Fourgoblin/documentAnalyzer](https://github.com/Fourgoblin/documentAnalyzer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Fourgoblin/documentAnalyzer.svg?style=for-the-badge
[contributors-url]: https://github.com/Fourgoblin/documentAnalyzer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Fourgoblin/documentAnalyzer.svg?style=for-the-badge
[forks-url]: https://github.com/Fourgoblin/documentAnalyzer/network/members
[stars-shield]: https://img.shields.io/github/stars/Fourgoblin/documentAnalyzer.svg?style=for-the-badge
[stars-url]: https://github.com/Fourgoblin/documentAnalyzer/stargazers
[issues-shield]: https://img.shields.io/github/issues/Fourgoblin/documentAnalyzer.svg?style=for-the-badge
[issues-url]: https://github.com/Fourgoblin/documentAnalyzer/issues
[license-shield]: https://img.shields.io/github/license/Fourgoblin/documentAnalyzer.svg?style=for-the-badge
[license-url]: https://github.com/Fourgoblin/documentAnalyzer/blob/master/LICENSE.txt
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
