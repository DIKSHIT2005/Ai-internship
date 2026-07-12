import requests

prompt = "generate a image of a falling man."
url = f"https://image.pollinations.ai/prompt/{prompt}"

print(f"Generating your image ... {prompt}")

response = requests.get(url)
print(response.status_code)

if response.status_code == 200:
    with open("goat.png", "wb") as f:
        f.write(response.content)
    print("Image generated successfully and saved as goat.png")
else:
    print("Failed to generate image. Status code:", response.status_code)
    print(response.text)