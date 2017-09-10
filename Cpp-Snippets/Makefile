UM_GCC_VERSION   = 6.2.0

PATH        	:= /usr/um/$(UM_GCC_VERSION)/bin:$(PATH)
LD_LIBRARY_PATH := /usr/um/$(UM_GCC_VERSION)/lib64
LD_RUN_PATH     := /usr/um/$(UM_GCC_VERSION)/lib64

TESTSRCS    = $(wildcard test*.cpp)
PROJSRCS    = $(wildcard project*.cpp)
SRCS        = $(wildcard *.cpp)
SRCS        = $(filter-out $(TESTSRCS), $(SRCS))
OBJS        = $(SRCS:%.cpp=%.o)
TARGETS     = 
TESTS       =

ZIPFILES    = $(SRCS) Makefile
ZIPFILENAME = submit.tar.gz

CC          = gcc
CCSTD       = -std=c99
CCWFLAGS    = -Wall -Wextra -Wshadow -Wpedantic --pedantic-errors -O2 $(CCSTD)
CCNFLAGS    = -Wno-unused-value -Wno-unused-parameter -Wno-attributes -Wno-unused-variable
CCGDBFLAGS  = -g
CCFLAGS     = $(CCWFLAGS) $(CCNFLAGS) $(CCGDBFLAGS)

CXX         = g++
CXXSTD      = -std=c++11
CXXWFLAGS   = -Wall -Wextra -Wshadow -Wpedantic --pedantic-errors -O2 $(CXXSTD)
CXXNFLAGS   = -Wno-unused-value -Wno-unused-parameter -Wno-attributes -Wno-unused-variable
CXXSANFLAGS = -fsanitize=undefined,address,leak,bounds,bool,enum
CXXGDBFLAGS = -g
CXXFLAGS    = $(CXXWFLAGS) $(CXXNFLAGS) $(CXXGDBFLAGS)

INCLUDES    = 
LDFLAGS     =
LIBS        =

RM          = rm -fv

release: CXXFLAGS += -O3 -DNDEBUG
release: all

debug: CXXFLAGS += -g3 -DDEBUG
debug: all

profile: CXXFLAGS += -pg
profile: clean all

all: $(TARGETS)

$(TARGETS): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $(TARGETS) $(OBJS) $(LDFLAGS) $(LIBS)

$(OBJS) : $(SRCS)
	$(CXX) $(CXXFLAGS) -c $**

.PHONY: all release debug profile clean alltests zip

.SUFFIXES:

zip:
	rm -f $(ZIPFILES)
	dos2unix $(ZIPFILES)
	tar -vcz $(ZIPFILES) -f $(ZIPFILENAME)

clean:
	$(RM) $(OBJS) $(TARGETS) $(TESTS) 

distclean: clean
	$(RM) $(TARGETS)

define make_tests
	SRCS = $$(filter-out $$(PROJECTSRCS), $$(SRCS))
	OBJS = $$(SRCS:%.cpp=%.o)
	HDRS = $$(wildcard *.h)
	$(1): CXXFLAGS += -g -DDEBUG
	$(1): $$(OBJS) $$(HDRS) $(1).cpp
	ifeq ($$(PROJECTSRCS),)
		@echo Edit PROJECTSRCS variable to .cpp file with main
		@exit 1
	endif
	$$(CXX) $$(CXXFLAGS) $$(OBJS) $(1).cpp -o $(1)
endef

# $(foreach test, $(TESTS), $(eval $(call make_tests, $(test))))

alltests: clean $(TESTS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $*.cpp

define MAKEFILE_HELP

endef
export MAKEFILE_HELP

help:
	@echo "$$MAKEFILE_HELP"