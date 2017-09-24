#include <thread>
#include <future>
#include <functional>
#include <memory>
#include <chrono>
#include <iostream>
#include <list>
using namespace std::chrono;

struct naive_future;

std::shared_ptr<naive_future> start_async(std::function<void()> fun);

struct naive_future : std::enable_shared_from_this<naive_future>
{
    std::future<void> future;
    std::mutex lock;
    bool finished = false;
    std::list<std::function<void()>> continuation;

    std::shared_ptr<naive_future> then(std::function<void()> fun)
    {
        std::lock_guard<std::mutex> guard(lock);
        continuation.push_back(std::move(fun));
        if (finished)
        {
            auto cont = std::move(continuation.front());
            continuation.pop_front();
            return start_async(std::move(cont));
        }
        return shared_from_this();
    }
};

void dot_then_wrapper(std::shared_ptr<naive_future> future, std::function<void()> fun)
{
    fun();
    {
        std::lock_guard<std::mutex> guard(future->lock);
        future->finished = true;
    }
    for (;;)
    {
        std::function<void()> cont;
        {
            std::lock_guard<std::mutex> guard(future->lock);
            if (!future->continuation.empty())
            {
                cont = std::move(future->continuation.front());
                future->continuation.pop_front();
            }
        }
        if (cont != nullptr)
        {
            cont();
        }
        else
        {
            return;
        }
    }
}

std::shared_ptr<naive_future> start_async(std::function<void()> fun)
{
    auto ret = std::make_shared<naive_future>();
    ret->future = std::async(dot_then_wrapper, ret, std::move(fun));

    return ret;
}


int main()
{
    auto task = start_async([]
    {
        std::cout << "start\n";
        std::this_thread::sleep_for(3s);
        std::cout << "3s passed\n";
    });
    std::this_thread::sleep_for(4s);
    std::cout << "main thread 4s passed\n";
    task->then([]
    {
        std::cout << "task execute immediately\n";
    })->then([]
    {
        std::this_thread::sleep_for(5s);
        std::cout << "task 5s passed\n";
    })->then([]
    {
        std::cout << "task end\n";
    })->future.wait();
    std::cout << "main end\n";
}