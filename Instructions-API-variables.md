
# How to add environment variables for API keys
1. In terminal:
    ```
    pip3 install python-dotenv
    ```

2. Create a .env file in your root directly that has the following text:
    ```python
    API=your_API_key_here
    ```


### Only required for initial code set up. 
3. Add these lines of code to your file. 
    ```python
    from dotenv import load_dotenv
    load_dotenv()
    ```

4. You can now access your variable using
    ```python
    api = os.environ['API']
    ```