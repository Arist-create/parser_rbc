FROM python:3.10.8
WORKDIR /app
ADD . /app
EXPOSE 8080
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install aiohttp            
RUN python3 -m pip install aiosignal          
RUN python3 -m pip install async-timeout     
RUN python3 -m pip install attrs              
RUN python3 -m pip install beautifulsoup4     
RUN python3 -m pip install certifi            
RUN python3 -m pip install charset-normalizer 
RUN python3 -m pip install frozenlist         
RUN python3 -m pip install idna               
RUN python3 -m pip install Markdown         
RUN python3 -m pip install multidict          
RUN python3 -m pip install pip                
RUN python3 -m pip install pyTelegramBotAPI   
RUN python3 -m pip install python-dotenv     
RUN python3 -m pip install requests           
RUN python3 -m pip install soupsieve          
RUN python3 -m pip install urllib3            
RUN python3 -m pip install yarl   
RUN python3 -m pip install asyncio
CMD [ "python3", "bot.py" ]