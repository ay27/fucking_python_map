## Fucking Python Map
由于multiprocessing的map函数对传入的函数要求是可pickle的，否则会抛出恶心的`PicklingError`。

然而很多时候我们确实想要用最少的改动完成并行，这个repo就是为此需要而生。

### 调用方法
result_list = async_run(func, iterable, process_count=cpu_count())

### 代码环境
python2 or python3
