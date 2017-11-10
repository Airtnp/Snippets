#include <utility>
#include <string>
#include <string_view>

// Another implementation
auto constexpr test_helper(...) {}
#define is_constexpr(...) noexcept(test_helper((__VA_ARGS__, 0)))


using namespace std::literals;

//

template <class F, class... Args,
    class = decltype(std::declval<F&&>()(std::declval<Args&&>()...))>
auto constexpr is_valid_impl(int)
-> std::true_type;

template <class F, class... Args>
auto constexpr is_valid_impl(...)
-> std::false_type;

template <class F>
constexpr auto is_valid(F&&)
{ 
    return [](auto&& ...args)
    {
        // non-constexpr, 
        // we cannot deduce auto_list<detail::checker::call<__VA_ARGS__>
        // since template non-type parameter must be constexpr
        return decltype(
            is_valid_impl<F&&, decltype(args)&&...>(int{})
        ){};
    };
}

//

namespace detail
{
    struct checker
    {
        auto static constexpr call(...)
        { return true; }
    };
}

template <auto...>
struct auto_list
{};


#define is_constexpr(...) \
    is_valid( \
        [](auto checker) \
            -> auto_list<decltype(checker)::call(__VA_ARGS__)> {} \
    )(detail::checker{})

//

auto constexpr func(...)
{}

int main()
{
    // empty check

    static_assert(is_constexpr());

    // literal values

    static_assert(is_constexpr("hello"));
    static_assert(is_constexpr("hello"sv));

    static_assert(!is_constexpr("hello"s));

    // constexpr values

    auto constexpr a = "hello";
    auto constexpr b = "hello"sv;    
    
    static_assert(is_constexpr(a));
    static_assert(is_constexpr(b));

    // non-constexpr values

    auto c = "hello";
    auto d = "hello"s;
    auto e = "hello"sv;
    
    static_assert(!is_constexpr(c));
    static_assert(!is_constexpr(d));
    static_assert(!is_constexpr(e));

    // non-capture lambda as literal (NOTE: relies on p0315)

    #if 0
    static_assert(is_constexpr([]{}));
    static_assert(is_constexpr([]{ return "hello"; }));
    static_assert(is_constexpr([]{ return "hello"sv; }));
    static_assert(is_constexpr([]{ return "hello"s; }));

    static_assert(is_constexpr([]{ return "hello"; }()));
    static_assert(is_constexpr([]{ return "hello"sv; }()));
    static_assert(is_constexpr([]{ return "hello"s; }()));
    #endif

    // capture lambda as literal (NOTE: relies on p0315)

    #if 0
    static_assert(is_constexpr([&]{}));
    static_assert(is_constexpr([&]{ return "hello"; }));
    static_assert(is_constexpr([&]{ return "hello"sv; }));
    static_assert(is_constexpr([&]{ return "hello"s; }));

    static_assert(is_constexpr([&]{ return "hello"; }()));
    static_assert(is_constexpr([&]{ return "hello"sv; }()));
    static_assert(is_constexpr([&]{ return "hello"s; }()));
    #endif

    // constexpr non-capture lambda

    auto constexpr lam1 = []{};
    auto constexpr lam2 = []{ return "hello"; };
    auto constexpr lam3 = []{ return "hello"sv; };
    auto constexpr lam4 = []{ return "hello"s; };

    static_assert(is_constexpr(lam1));
    static_assert(is_constexpr(lam2));
    static_assert(is_constexpr(lam3));
    static_assert(is_constexpr(lam4));

    static_assert(is_constexpr(lam2()));
    static_assert(is_constexpr(lam3()));
    static_assert(!is_constexpr(lam4()));

    // non-constexpr non-capture lambda

    auto lam5 = []{};
    auto lam6 = []{ return "hello"; };
    auto lam7 = []{ return "hello"sv; };
    auto lam8 = []{ return "hello"s; };

    static_assert(is_constexpr(lam5));
    static_assert(is_constexpr(lam6));
    static_assert(is_constexpr(lam7));
    static_assert(is_constexpr(lam8));

    static_assert(is_constexpr(lam6()));
    static_assert(is_constexpr(lam7()));
    static_assert(!is_constexpr(lam8()));

    // constexpr capture lambda

    auto constexpr cap1 = [&]{};
    auto constexpr cap2 = [&]{ return a; };
    auto constexpr cap3 = [&]{ return b; };

    static_assert(is_constexpr(cap1));
    static_assert(is_constexpr(cap2));
    static_assert(is_constexpr(cap3));

    static_assert(is_constexpr(cap2()));
    static_assert(is_constexpr(cap3()));

    // non-constexpr capture lambda

    auto cap4 = [&]{};
    auto cap5 = [&]{ return c; };
    auto cap6 = [&]{ return d; };
    auto cap7 = [&]{ return e; };

    static_assert(is_constexpr(cap4));
    static_assert(!is_constexpr(cap5));
    static_assert(!is_constexpr(cap6));
    static_assert(!is_constexpr(cap7));

    static_assert(!is_constexpr(cap5()));
    static_assert(!is_constexpr(cap6()));
    static_assert(!is_constexpr(cap7()));

    //
}