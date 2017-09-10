/*
*	Module Name:
*		antidebug_long_int3.cpp
*
*	Abstract:
*		Attempts to detect the presence of a debugger
*		by issuing a multi-byte int 3 and inspecting 
*		page PTE mappings.
*
*	Author:
*		Nemanja (Nemi) Mulasmajic <nm@triplefault.io>
*			http://triplefault.io
*/
// ref: http://www.triplefault.io/2017/08/detecting-debuggers-by-abusing-bad.html

#pragma warning(disable: 4710)

#pragma warning(push, 0)
#include <windows.h>
#include <stdio.h>
#include <Psapi.h>
#pragma warning(pop)

#pragma comment(lib, "psapi.lib")

// The size of an architecture page on x86/x64.
#define PAGE_SIZE 0x1000

// A pseudo-handle that represents the current process.
#define NtCurrentProcess() ((HANDLE)-1)

// Multi-byte int 3.
BYTE _LongInt3[] = { 0xCD, 0x03 };

int main(void)
{
	int status = -1;
	
	// We allocate 2 contiguous pages of executable virtual memory.
	PBYTE Memory = (PBYTE)VirtualAlloc(NULL, (PAGE_SIZE * 2), (MEM_COMMIT | MEM_RESERVE), PAGE_EXECUTE_READWRITE);
	if (!Memory)
	{
		fprintf(stderr, "[-] ERROR: Failed to allocate memory.\n");
		goto Cleanup;
	}

	// The first page, "page 1", will have the multi-byte form of int 3 
	// embedded at the very end of the page. This is done so that the next 
	// byte immediately after the multi-byte int 3 will span into "page 2".
	//
	// e.g:

	//	| Page 1						| Page 2
	//	[.....................0xCD 0x03][............................]

	PBYTE CodeLocation = &Memory[PAGE_SIZE - sizeof(_LongInt3)];
	PBYTE DeadPageLocation = &Memory[PAGE_SIZE];

	// Add the int 3 to the very end of page 1.
	memcpy(CodeLocation, _LongInt3, sizeof(_LongInt3));

	// Page 2 should never be accessed and therefore should not be 
	// present in our process' working set. 
	PSAPI_WORKING_SET_EX_INFORMATION wsi;
	wsi.VirtualAddress = DeadPageLocation;
	if (!QueryWorkingSetEx(NtCurrentProcess(), &wsi, sizeof(wsi)))
	{
		fprintf(stderr, "[-] ERROR: QueryWorkingSetEx failed with error: 0x%lx.\n", GetLastError());
		goto Cleanup;
	}

	if (wsi.VirtualAttributes.Valid)
	{
		fprintf(stderr, "[-] ERROR: Page is expected to be invalid. Make sure you have not inadvertently accessed this page.\n");
		goto Cleanup;
	}
	
	__try
	{
		// Invoke the long form of int 3.
		((void(*)())CodeLocation)();
	}
	__except (EXCEPTION_EXECUTE_HANDLER) { }

	// If a debugger caught the exception, even if it was passed to the 
	// application via "go unhandled", it will have, most likely, mapped
	// page 2 into the application's memory space.
	if (!QueryWorkingSetEx(NtCurrentProcess(), &wsi, sizeof(wsi)))
	{
		fprintf(stderr, "[-] ERROR: QueryWorkingSetEx failed with error: 0x%lx.\n", GetLastError());
		goto Cleanup;
	}

	printf("[+] Debugger %s.\n", ((wsi.VirtualAttributes.Valid) ? "detected" : "not detected"));

	status = 0;

Cleanup:
	
	// Free allocated memory.
	if (Memory)
	{
		VirtualFree(Memory, 0, MEM_FREE);
		Memory = NULL;
	}

	// Wait for [ENTER] key press to terminate the program.
	getchar();

	return status;
}