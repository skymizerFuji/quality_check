# To run the benchmark

Activate the environment:
```
source .venv/bin/activate
```



## Then in another terminal
- vp1902
First you have to launch the server
```
python openai_server.py
```

Then run the benchmark:
```
python benchmark.py -m Qwen/Qwen2.5-1.5B-Instruct -i zh -o quantized
```

- dl02
First you have to launch the server
```
./llama_server_<replace_with_dataaset_name>.sh
```

Then run the benchmark:
```
```
python benchmark.py -m Qwen/Qwen2.5-1.5B-Instruct -i zh -o unquantized
```
