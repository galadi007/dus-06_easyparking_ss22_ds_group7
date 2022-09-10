# dus-06_easyparking_ss22_ds_group7
# Readme for the file "easyparking_pyngrok_in_progress.ipynb"

in general: we are setting up a tunnel via ngrok to show our locally hosted application-content via public url.
Ngrok is a useful utility for creating secure tunnels for locally hosted applications using a reverse proxy.
It is a utility to make locally hosted applications available over the web.

This leads to a solution, that google colab users can also build a frontend UI available over the web without the need to install any programms on their device.

1. install streamlit to use the with streamlit created UI 
2. create an app.py, the information given here will be shown on a webpage. Example with plain text 'Hello World'
3. ngrok instsallation for tunneling, using Pyngrok as wrapper for ngrok that makes ngrok readily available from anywhere on the command line 
4. set ngrok auth token. Get your auth thoken for free after registering at ngrok.com/dashboard
5. building the public URL via ngrok for our localhost port80

