import scanner

tokens = scanner.Scanner('n = 1.;1.12 Hello "hello" return "return"\nprint class Object();fun\n"some//" //false').scan_tokens()
for token in tokens:
    print token