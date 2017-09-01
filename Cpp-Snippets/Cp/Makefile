all: template

template: template.cpp
	g++ -std=c++11 -O2 -Wall -Wextra -Wpedantic -Wshadow template.cpp -o bin

run: bin
	./bin