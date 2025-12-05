
# Install promptfoo

Make sure you have Node.js >= 20.0 installed.

```
npm install -g promptfoo
promptfoo --version
```

# To run the benchmark

Ensure you have set openai api key in your environment variables

launch the server
```
python promptfoo/openai_server.py
```
and run
```
cd promptfoo
./eval_vp1902.sh
```

# To view the results

```
./promptfoo/view.sh
```
