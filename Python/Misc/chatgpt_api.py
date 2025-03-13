from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a highly intelligent system."},
    {"role": "user", "content": "Explain the concept of love."}
  ]
)

print(completion.choices[0].message)
