# <img src="https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg" width="35px" alt="Bard Icon" /> Bard-WebAPI

Reverse Engineered Async API for Google Bard

## Installation

```bash
pip install bard-webapi
```

## Authentication

- Go to <https://bard.google.com/> and login with your Google account
- Press F12 for web inspector, go to `Network` tab and refresh the page
- Click any request and copy cookie values of `__Secure-1PSID` and `__Secure-1PSIDTS`

## Usage

### Initialization

```python
from bard_webapi import BardClient

Secure_1PSID = [COOKIE VALUE HERE]
Secure_1PSIDTS = [COOKIE VALUE HERE]

client = BardClient(Secure_1PSID, Secure_1PSIDTS, proxy=None)
await client.init()
```

### Generate contents from text inputs

```python
response = await client.generate_content("Hello World!")
print(response.text)
```

### Conversations across multiple turns

```python
chat = client.start_chat()
response1 = await chat.send_message("Briefly introduce Europe")
response2 = await chat.send_message("What's the population there?")
print(response1.text, response2.text, sep="\n----------------------------------\n")
```

### Retrieve images in response

```python
response = await client.generate_content("Send me some pictures of cats")
images = response.images
for image in images:
    print(f"{image.title}({image.url}) - {image.alt}", sep="\n")
```

### Check Other Answer Choices

```python
response = await client.generate_content("What's the best Japanese dish in your mind? Choose one only.")
candidates = response.candidates
for candidate in candidates:
    print(candidate, "\n----------------------------------\n")
```
