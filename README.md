## Requirements
- your computer need to have ollama install ( download [ollama](https://ollama.com/)  and start any model based on your os )
  I start llama2 model, you can also start other models from [here](https://ollama.com/library) 
  ```bash
  ollama run llama2
  ```
## How to start
1. create a virtual environment
   ``` bash
   python -m venv venv
   ```
2. activate venv
   ```bash
   ## window
   venv\Scripts\activate

   ## macos / linux
   source venv/bin/activate
   ```

Note** : if you are using window change this line 

`pipe = pipe.to("mps")` to `pipeline.to("cuda")`

3. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
4. run streamlit app
   ```bash
   streamlit run app.py
   ```
