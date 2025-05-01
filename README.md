<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/Fourgoblin/documentAnalyzer">
  </a>

<h3 align="center">Document Analysis Tool</h3>

  <p align="center">
    The goal of this project is to create a program that can accurately segment an image of a document. The program will provide coordinates of the found content segements in JSON format, with each segment seperated by whitespace within the document being analyzed.
    <br />
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
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is being developed for OpenText by CS499 students at the University of Kentucky.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
* ![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=opencv&logoColor=white)
* ![Tesseract OCR](https://img.shields.io/badge/Tesseract-1769aa?style=for-the-badge&logo=tesseract&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

For the fastest setup simply download the executable: [https://github.com/Fourgoblin/documentAnalyzer/releases/tag/v1.5.3](https://github.com/Fourgoblin/documentAnalyzer/releases/tag/v1.5.3)

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

The application currently handles most common types of image files. PDF handling is in development. To use the tool upload a file and use the threshold sliders to adjust to the desired sections. Click and drag the adjustable boxes if any sections need to be adjusted. A JSON file containing document section data will be placed in an "output" directory.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Landon Kuerzi - ldkuer01@gmail.com, Andrew Mortimer - andrewmortimer929@gmail.com, Sharan Ravula - sharan4117@gmail.com, Jovani Rivas - Jovanirivas14@gmail.com, Mason Zande - masonzande@live.com

Project Link: [https://github.com/Fourgoblin/documentAnalyzer](https://github.com/Fourgoblin/documentAnalyzer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
