#include <utility>
#include <type_traits>

struct dummy {
    template<class... Ts>
    dummy(Ts&&...) {}
    template<class T>
    typename std::enable_if<(bool)T(), dummy>::type
    operator&&(T);
};

#define CAT_(A,...)A##__VA_ARGS__
#define CAT(A,...) CAT_(A,__VA_ARGS__)

#define CONCEPT_def(TPARAM, NAME, ...)\
    struct CAT(CAT(CONCEPT_, NAME), Concept) {\
        CAT(CONCEPT_, TPARAM) auto requires_ CAT(CONCEPT_, __VA_ARGS__) );\
    };\
    CAT(CONCEPT_, TPARAM)\
    using CAT(CONCEPT_, NAME) =\
        models<\
            CAT(CAT(CONCEPT_, NAME), Concept),\
            CAT(CONCEPT_AUX_, TPARAM)

#define CONCEPT_template(...) template<__VA_ARGS__>
#define CONCEPT_requires(...) (__VA_ARGS__) -> decltype(dummy
#define CONCEPT_concept
#define CONCEPT_PP_class
#define CONCEPT_PP_typename
#define CAT2_(A,...) A ## __VA_ARGS__
#define CAT2(A,...) CAT2_(A,__VA_ARGS__)
#define CONCEPT_AUX_template(...) \
    CAT2(CONCEPT_PP_TPARAM_, CONCEPT_PP_COUNT(__VA_ARGS__, 5, 4, 3, 2, 1))(__VA_ARGS__)>
#define CONCEPT_PP_COUNT(_a, _b, _c, _d, _e, ...) CONCEPT_PP_COUNT_2_(__VA_ARGS__, ~, ~, ~, ~, ~)
#define CONCEPT_PP_COUNT_2_(_a, _b, _c, _d, _e, ...) _a
#define CONCEPT_PP_TPARAM_1(_1, ...) CAT2(CONCEPT_PP_, _1)
#define CONCEPT_PP_TPARAM_2(_1, ...) CAT2(CONCEPT_PP_, _1), CONCEPT_PP_TPARAM_1(__VA_ARGS__)
#define CONCEPT_PP_TPARAM_3(_1, ...) CAT2(CONCEPT_PP_, _1), CONCEPT_PP_TPARAM_2(__VA_ARGS__)
#define CONCEPT_PP_TPARAM_4(_1, ...) CAT2(CONCEPT_PP_, _1), CONCEPT_PP_TPARAM_3(__VA_ARGS__)
#define CONCEPT_PP_TPARAM_5(_1, ...) CAT2(CONCEPT_PP_, _1), CONCEPT_PP_TPARAM_4(__VA_ARGS__)

template<class T, class...Args>
struct models
{
    template<class C = T,
        class = decltype(&C::template requires_<Args...>)>
    constexpr operator bool() const { return true; }
    constexpr operator bool() const volatile { return false; }
};

CONCEPT_def(
    template(class T, class U),
    concept ConvertibleTo,
        requires (T(&p)()) {
            static_cast<U>(p())
        } && std::is_convertible<T, U>()
);

static_assert(ConvertibleTo<int, short>(), "");
static_assert(!ConvertibleTo<int*, short>(), "");

