package main

import fmt "fmt"  // Package implementing formatted I/O.
import (
    "os"
    "flag"  // command line option parser
)

func PrintString() {
	const (
		Space = " "
	)
	s := "Foo"
    fmt.Printf("%v%vBar\n", s, Space)
}

func main() {
	flag.Parse()
	s := ""
	for i := 0; i < flag.NArg(); i++ {
		s += flag.Arg(i) + " "
	}
	os.Stdout.WriteString(s)

	var a[4] int;
	a[0] = 12;
    fmt.Printf("Hello, %v\n", a[0])

	// Arrays
	b := [2]string{"Penn", "Teller"}
    fmt.Printf("Hello, %v\n", b[0])

	c := [...]string{"Penn", "Teller"}
    fmt.Printf("Hello, %v\n", c[1])

	// Slices
	d := []string{"Penn", "Teller"}
    fmt.Printf("Hello, %v\n", d[0])

	e := []string{"Penn", "Teller"}
    fmt.Printf("Hello, %v\n", e[1])
}

