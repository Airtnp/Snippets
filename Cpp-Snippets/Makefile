
PATH        	:= $(PATH)
LIBRARY_PATH    := $(LIBRARY_PATH)
LD_LIBRARY_PATH := $(LD_LIBRARY_PATH)
LD_RUN_PATH     := $(LD_RUN_PATH)

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
CXXSTD      = -std=c++17
CXXOPFLAGS  = -Ofast -DNDEBUG \
			  -march=native \
			  -fwhole-program -flto \
			  -fprefetch-loop-arrays \
			  -Wno-coverage-mismatch \
			  -fno-rtti \
			  -fomit-frame-pointer \
			  -falign-functions=16 -falign-loops=16
CXXWFLAGS   = -Wall -Wextra -Wshadow -Wpedantic --pedantic-errors $(CXXSTD)
CXXNFLAGS   = -Wno-unused-value -Wno-unused-parameter -Wno-attributes -Wno-unused-variable
CXXSANFLAGS = -fsanitize=undefined,address,leak,bounds,bool,enum
CXXDBFLAGS  = -g3 -Og -DDEBUG
CXXFLAGS    = $(CXXWFLAGS) $(CXXNFLAGS)

INCLUDES    = 
LDFLAGS     =
LIBS        =

RM          = rm -fv

# make release - will compile "all" with $(CXXFLAGS) and the -O3 flag
#				 also defines NDEBUG so that asserts will not check
release: CXXFLAGS += $(CXXOPFLAGS) -fprofile-use
release: all

prerelease: CXXFLAGS += -O3 -DNDEBUG
prerelease: all

# make debug - will compile "all" with $(CXXFLAGS) and the -g flag
#              also defines DEBUG so that "#ifdef DEBUG /*...*/ #endif" works
debug: EXECUTABLE := $(DEBUG)
debug: CXXFLAGS += $(CXXDBFLAGS)
debug: clean all

# make profile - will compile "all" with $(CXXFLAGS) and the -pg flag
profile: CXXFLAGS += $(CXXOPFLAGS) -fprofile-generate
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