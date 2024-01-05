[![Python application test with Github Actions](https://github.com/yrangana/Strategy_Pattern_Calculator/actions/workflows/main.yml/badge.svg)](https://github.com/yrangana/Strategy_Pattern_Calculator/actions/workflows/main.yml)

# Strategy Pattern Calculator
Python implementation of a command line calculator using the strategy design pattern 

## Description
This is a simple command-line calculator that can perform basic arithmetic operations. The calculator is implemented using the strategy design pattern. The calculator can perform the following operations:

- Addition
- Subtraction
- Multiplication
- Division

### To be implemented:

- Setup tool to install the calculator as a package
- Exponentiation
- Square root
- Logarithm

## Getting Started

### Installing
- Clone the repository
```
git clone https://github.com/yrangana/Strategy_Pattern_Calculator.git
```
- Install the dependencies
```
make install
```

### Executing program in python

- Run the calculator with prompts
```
python src/main.py
```

- Run the calculator with arguments
```
python src/main.py -n1 <first number> -n2 <second number> -op <operation>
```

- Run the tests
```
make test
```

### Executing program in CLI

- Setup as a Command Line Tool
```
python -m pip install --editable .
```

- Run the calculator with prompts
```
spcalc
```

- Run the calculator with arguments
```
spcalc -n1 <first number> -n2 <second number> -op <operation>
```



## Help

```
Usage: main.py [OPTIONS]

Options:
  -n1, --num1 FLOAT               First number
  -n2, --num2 FLOAT               Second number
  -op, --operation [add|subtract|multiply|divide]
                                  Operation to perform
  --help                          Show this message and exit.
```

## Authors
[Yasiru Rangana](https://github.com/yrangana)

## Version History
* V1.0.0
    * [Initial Release as a Command Line Tool](https://github.com/yrangana/Strategy_Pattern_Calculator/releases/tag/V1.0.0)
* V1.1.0
    * [Minor Bugs were fixed](https://github.com/yrangana/Strategy_Pattern_Calculator/releases/tag/V1.1.0)
 
* V1.2.0
    * [Minor Improvements](https://github.com/yrangana/Strategy_Pattern_Calculator/releases/tag/V1.2.0)

## License
This project is licensed under the MIT License - see the [License](LICENSE) file for details
