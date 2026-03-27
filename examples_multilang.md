# 🌐 Ejemplos de Consumo del Endpoint en Múltiples Lenguajes

Ejemplos prácticos de cómo consumir el endpoint de Chatterbox Multilingual TTS desde diferentes lenguajes de programación.

## 📋 Configuración Común

Antes de empezar, necesitas:
- **ENDPOINT_URL**: URL de tu endpoint (ej: `https://xxx.endpoints.huggingface.cloud`)
- **HF_TOKEN**: Tu token de Hugging Face

## Python 🐍

### Usando requests (básico)

```python
import requests
import base64

ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
HF_TOKEN = "your_token_here"

def generate_tts(text, language="en"):
    response = requests.post(
        ENDPOINT_URL,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "inputs": text,
            "parameters": {
                "language_id": language,
                "exaggeration": 0.5,
                "temperature": 0.8
            }
        }
    )
    
    result = response.json()
    
    if "audio" in result:
        audio_data = base64.b64decode(result["audio"])
        with open(f"output_{language}.wav", "wb") as f:
            f.write(audio_data)
        print(f"✅ Audio guardado: output_{language}.wav")
    else:
        print(f"❌ Error: {result.get('error')}")

# Uso
generate_tts("Hello world", "en")
generate_tts("Hola mundo", "es")
```

### Usando httpx (async)

```python
import httpx
import base64
import asyncio

ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
HF_TOKEN = "your_token_here"

async def generate_tts_async(text, language="en"):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            ENDPOINT_URL,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": text,
                "parameters": {"language_id": language}
            },
            timeout=60.0
        )
        
        result = response.json()
        
        if "audio" in result:
            audio_data = base64.b64decode(result["audio"])
            filename = f"output_{language}.wav"
            with open(filename, "wb") as f:
                f.write(audio_data)
            return filename
        else:
            raise Exception(result.get("error"))

# Uso
async def main():
    tasks = [
        generate_tts_async("Hello", "en"),
        generate_tts_async("Hola", "es"),
        generate_tts_async("Bonjour", "fr")
    ]
    results = await asyncio.gather(*tasks)
    print(f"Generados: {results}")

asyncio.run(main())
```

## JavaScript / Node.js 🟨

### Usando axios

```javascript
const axios = require('axios');
const fs = require('fs');

const ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud";
const HF_TOKEN = "your_token_here";

async function generateTTS(text, language = 'en') {
    try {
        const response = await axios.post(
            ENDPOINT_URL,
            {
                inputs: text,
                parameters: {
                    language_id: language,
                    exaggeration: 0.5,
                    temperature: 0.8
                }
            },
            {
                headers: {
                    'Authorization': `Bearer ${HF_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        if (response.data.audio) {
            const audioBuffer = Buffer.from(response.data.audio, 'base64');
            const filename = `output_${language}.wav`;
            fs.writeFileSync(filename, audioBuffer);
            console.log(`✅ Audio guardado: ${filename}`);
            return filename;
        } else {
            console.error(`❌ Error: ${response.data.error}`);
        }
    } catch (error) {
        console.error(`❌ Request failed: ${error.message}`);
    }
}

// Uso
generateTTS("Hello world", "en");
generateTTS("Hola mundo", "es");
```

### Usando fetch (navegador)

```javascript
const ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud";
const HF_TOKEN = "your_token_here";

async function generateTTS(text, language = 'en') {
    try {
        const response = await fetch(ENDPOINT_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${HF_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                inputs: text,
                parameters: {
                    language_id: language
                }
            })
        });

        const result = await response.json();

        if (result.audio) {
            // Convertir base64 a blob
            const audioData = atob(result.audio);
            const audioArray = new Uint8Array(audioData.length);
            for (let i = 0; i < audioData.length; i++) {
                audioArray[i] = audioData.charCodeAt(i);
            }
            const blob = new Blob([audioArray], { type: 'audio/wav' });
            
            // Crear URL y reproducir
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.play();
            
            // O descargar
            const a = document.createElement('a');
            a.href = audioUrl;
            a.download = `output_${language}.wav`;
            a.click();
            
            console.log('✅ Audio generado');
        } else {
            console.error('❌ Error:', result.error);
        }
    } catch (error) {
        console.error('❌ Request failed:', error);
    }
}

// Uso
generateTTS("Hello world", "en");
```

## PHP 🐘

```php
<?php

$ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud";
$HF_TOKEN = "your_token_here";

function generateTTS($text, $language = 'en') {
    global $ENDPOINT_URL, $HF_TOKEN;
    
    $data = [
        'inputs' => $text,
        'parameters' => [
            'language_id' => $language,
            'exaggeration' => 0.5,
            'temperature' => 0.8
        ]
    ];
    
    $ch = curl_init($ENDPOINT_URL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $HF_TOKEN,
        'Content-Type: application/json'
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        $result = json_decode($response, true);
        
        if (isset($result['audio'])) {
            $audioData = base64_decode($result['audio']);
            $filename = "output_{$language}.wav";
            file_put_contents($filename, $audioData);
            echo "✅ Audio guardado: {$filename}\n";
            return $filename;
        } else {
            echo "❌ Error: " . ($result['error'] ?? 'Unknown error') . "\n";
        }
    } else {
        echo "❌ HTTP Error: {$httpCode}\n";
    }
}

// Uso
generateTTS("Hello world", "en");
generateTTS("Hola mundo", "es");

?>
```

## Go 🐹

```go
package main

import (
    "bytes"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

const (
    ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
    HF_TOKEN     = "your_token_here"
)

type TTSRequest struct {
    Inputs     string                 `json:"inputs"`
    Parameters map[string]interface{} `json:"parameters"`
}

type TTSResponse struct {
    Audio      string `json:"audio"`
    SampleRate int    `json:"sample_rate"`
    Language   string `json:"language"`
    Text       string `json:"text"`
    Error      string `json:"error,omitempty"`
}

func generateTTS(text, language string) error {
    request := TTSRequest{
        Inputs: text,
        Parameters: map[string]interface{}{
            "language_id":  language,
            "exaggeration": 0.5,
            "temperature":  0.8,
        },
    }

    jsonData, err := json.Marshal(request)
    if err != nil {
        return err
    }

    req, err := http.NewRequest("POST", ENDPOINT_URL, bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }

    req.Header.Set("Authorization", "Bearer "+HF_TOKEN)
    req.Header.Set("Content-Type", "application/json")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return err
    }

    var result TTSResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return err
    }

    if result.Error != "" {
        return fmt.Errorf("API error: %s", result.Error)
    }

    audioData, err := base64.StdEncoding.DecodeString(result.Audio)
    if err != nil {
        return err
    }

    filename := fmt.Sprintf("output_%s.wav", language)
    if err := ioutil.WriteFile(filename, audioData, 0644); err != nil {
        return err
    }

    fmt.Printf("✅ Audio guardado: %s\n", filename)
    return nil
}

func main() {
    if err := generateTTS("Hello world", "en"); err != nil {
        fmt.Printf("❌ Error: %v\n", err)
    }
    
    if err := generateTTS("Hola mundo", "es"); err != nil {
        fmt.Printf("❌ Error: %v\n", err)
    }
}
```

## Ruby 💎

```ruby
require 'net/http'
require 'json'
require 'base64'

ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
HF_TOKEN = "your_token_here"

def generate_tts(text, language = 'en')
  uri = URI(ENDPOINT_URL)
  
  request = Net::HTTP::Post.new(uri)
  request['Authorization'] = "Bearer #{HF_TOKEN}"
  request['Content-Type'] = 'application/json'
  request.body = {
    inputs: text,
    parameters: {
      language_id: language,
      exaggeration: 0.5,
      temperature: 0.8
    }
  }.to_json

  response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
    http.request(request)
  end

  result = JSON.parse(response.body)

  if result['audio']
    audio_data = Base64.decode64(result['audio'])
    filename = "output_#{language}.wav"
    File.write(filename, audio_data, mode: 'wb')
    puts "✅ Audio guardado: #{filename}"
    filename
  else
    puts "❌ Error: #{result['error']}"
    nil
  end
rescue => e
  puts "❌ Request failed: #{e.message}"
  nil
end

# Uso
generate_tts("Hello world", "en")
generate_tts("Hola mundo", "es")
```

## cURL 🔧

### Básico

```bash
curl -X POST "https://your-endpoint.endpoints.huggingface.cloud" \
  -H "Authorization: Bearer YOUR_HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "Hello world",
    "parameters": {
      "language_id": "en"
    }
  }' | jq -r '.audio' | base64 -d > output.wav
```

### Con parámetros completos

```bash
curl -X POST "https://your-endpoint.endpoints.huggingface.cloud" \
  -H "Authorization: Bearer YOUR_HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "Este es un ejemplo con parámetros personalizados",
    "parameters": {
      "language_id": "es",
      "exaggeration": 0.7,
      "temperature": 0.9,
      "cfg_weight": 0.5,
      "seed": 42
    }
  }' | jq -r '.audio' | base64 -d > output_es.wav
```

### Script bash para múltiples idiomas

```bash
#!/bin/bash

ENDPOINT_URL="https://your-endpoint.endpoints.huggingface.cloud"
HF_TOKEN="your_token_here"

declare -A texts=(
    ["en"]="Hello world"
    ["es"]="Hola mundo"
    ["fr"]="Bonjour le monde"
    ["de"]="Hallo Welt"
)

for lang in "${!texts[@]}"; do
    echo "Generando audio para: $lang"
    
    curl -X POST "$ENDPOINT_URL" \
      -H "Authorization: Bearer $HF_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"inputs\": \"${texts[$lang]}\",
        \"parameters\": {
          \"language_id\": \"$lang\"
        }
      }" | jq -r '.audio' | base64 -d > "output_$lang.wav"
    
    echo "✅ Guardado: output_$lang.wav"
done
```

## C# / .NET 🔷

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.IO;

class ChatterboxTTSClient
{
    private readonly string endpointUrl;
    private readonly string hfToken;
    private readonly HttpClient client;

    public ChatterboxTTSClient(string endpointUrl, string hfToken)
    {
        this.endpointUrl = endpointUrl;
        this.hfToken = hfToken;
        this.client = new HttpClient();
        this.client.DefaultRequestHeaders.Add("Authorization", $"Bearer {hfToken}");
    }

    public async Task<string> GenerateTTS(string text, string language = "en")
    {
        var request = new
        {
            inputs = text,
            parameters = new
            {
                language_id = language,
                exaggeration = 0.5,
                temperature = 0.8
            }
        };

        var json = JsonSerializer.Serialize(request);
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        try
        {
            var response = await client.PostAsync(endpointUrl, content);
            response.EnsureSuccessStatusCode();

            var responseBody = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<JsonElement>(responseBody);

            if (result.TryGetProperty("audio", out var audioElement))
            {
                var audioBase64 = audioElement.GetString();
                var audioData = Convert.FromBase64String(audioBase64);
                
                var filename = $"output_{language}.wav";
                await File.WriteAllBytesAsync(filename, audioData);
                
                Console.WriteLine($"✅ Audio guardado: {filename}");
                return filename;
            }
            else if (result.TryGetProperty("error", out var errorElement))
            {
                Console.WriteLine($"❌ Error: {errorElement.GetString()}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Request failed: {ex.Message}");
        }

        return null;
    }
}

// Uso
class Program
{
    static async Task Main(string[] args)
    {
        var client = new ChatterboxTTSClient(
            "https://your-endpoint.endpoints.huggingface.cloud",
            "your_token_here"
        );

        await client.GenerateTTS("Hello world", "en");
        await client.GenerateTTS("Hola mundo", "es");
    }
}
```

## 🎯 Notas Importantes

1. **Timeout**: Configura un timeout adecuado (30-60 segundos) ya que la generación puede tomar tiempo
2. **Rate Limiting**: Implementa retry logic para manejar límites de tasa
3. **Error Handling**: Siempre verifica si la respuesta contiene el campo `error`
4. **Base64**: El audio viene codificado en base64, debes decodificarlo antes de guardarlo
5. **Formato**: El audio retornado es WAV a 24kHz

## 📚 Recursos

- [ENDPOINT_USAGE.md](./ENDPOINT_USAGE.md) - Documentación completa de la API
- [example_client.py](./example_client.py) - Cliente Python completo
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía de deployment
