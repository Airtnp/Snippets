// ref: https://www.zhihu.com/question/66360542/answer/244544302

// ============================================================================================== //
// Bypass caller check varargs (cdecl) wrapper                                                    //
// ============================================================================================== //
template<typename T>
constexpr std::size_t SizeOfPack()
{
    return sizeof(T);
}

template<typename T, typename U, typename... RestT>
constexpr std::size_t SizeOfPack()
{
    return sizeof(T) + SizeOfPack<U, RestT...>();
}

template<typename RetT, typename... ArgsT>
struct VarargsCallWrapperHelper
{
    static const std::size_t kArgsSize = SizeOfPack<ArgsT...>();
    static void* func;
    static const void* kReturnHelperInstruction;
    static void* MyPlaceAddr;
    static void** JmpTarget;

    static RetT __cdecl Jumper(ArgsT... args, ...) noexcept;


    template<typename... VarArgsT>
    static RetT Call(ArgsT... args, VarArgsT... va) noexcept
    {
        RetT result;
        auto argsSize = kArgsSize/*variadic*/ + SizeOfPack<VarArgsT...>();
        auto backupJmpTarget = *JmpTarget;
        __asm mov eax, myplace;
        __asm mov[MyPlaceAddr], eax;
        *JmpTarget = MyPlaceAddr;
        Jumper(args..., va...);
    myplace:
        __asm add esp, [argsSize];
        __asm mov[result], eax;
        *JmpTarget = backupJmpTarget;
        return result;
    }
    RESTORE_ALL_CODE_ANALYSIS_WARNINGS
};

template<typename RetT, typename... ArgsT>
void * VarargsCallWrapperHelper<RetT, ArgsT...>::func = nullptr;

template<typename RetT, typename... ArgsT>
void * VarargsCallWrapperHelper<RetT, ArgsT...>::MyPlaceAddr = nullptr;

template<typename RetT, typename... ArgsT>
void** VarargsCallWrapperHelper<RetT, ArgsT...>::JmpTarget = (void**)GameAdd(IDA___IMP_D3DCOMPILE);//HOTS 42958

template<typename RetT, typename... ArgsT>
const void * VarargsCallWrapperHelper<RetT, ArgsT...>::kReturnHelperInstruction = (const void*)GameAdd(IDA_D3DCOMPILE);//HOTS 42958


/* Stack when entering function
--------------------------
| game fake instruction  |  ESP+0h must be instruction within game code segment
--------------------------
| vararg call stack N    |
--------------------------
| vararg call stack N - 1|
--------------------------
| ...                    |
--------------------------
| vararg call stack 1    |
--------------------------
*/

template<typename RetT, typename... ArgsT>
RetT _declspec(naked) __stdcall VarargsCallWrapperHelper<RetT, ArgsT...>::Jumper(ArgsT..., ...) noexcept
{
    __asm
    {
        add esp, 4;
        push kReturnHelperInstruction;
        push func;  //jump
        retn;
    }
}

//Call wrapper function
template<typename RetT, typename... ArgsT, typename... VarArgsT>
RetT VarargsCallWrapper(void* funcAddr, ArgsT.../*copy intended*/ args, VarArgsT... va)
{
    using WrapperT = VarargsCallWrapperHelper<RetT, ArgsT...>;
    WrapperT::func = funcAddr;
    return WrapperT::Call(std::move(args)..., va...);
}