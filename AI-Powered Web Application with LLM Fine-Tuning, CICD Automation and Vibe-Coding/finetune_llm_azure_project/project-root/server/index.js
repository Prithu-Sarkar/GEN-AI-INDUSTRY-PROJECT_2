import express from 'express';
import cors from 'cors';
import { AzureOpenAI } from 'openai';

const app = express();
app.use(cors()); app.use(express.json());

app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.post('/api/chat', async (req, res) => {
  const { messages, apiKey, endpoint, deployment, systemPrompt } = req.body;
  if (!apiKey || !endpoint || !deployment) return res.status(400).json({ error: 'Missing apiKey, endpoint, or deployment' });
  try {
    const client = new AzureOpenAI({ apiVersion: '2024-12-01-preview', endpoint, apiKey });
    const allMessages = [{ role: 'system', content: systemPrompt || 'You are a helpful customer support assistant.' }, ...messages];
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');
    res.flushHeaders();
    const stream = await client.chat.completions.create({ stream: true, messages: allMessages, max_tokens: 4096, temperature: 0.7, top_p: 1.0, model: deployment });
    for await (const chunk of stream) {
      if (chunk.choices && chunk.choices[0]) {
        const delta = chunk.choices[0].delta;
        if (delta && delta.content) res.write(`data: ${JSON.stringify({ content: delta.content })}\n\n`);
        if (chunk.choices[0].finish_reason === 'stop') res.write('data: [DONE]\n\n');
      }
    }
    res.end();
  } catch (err) {
    const msg = err?.message || 'Unknown error';
    if (!res.headersSent) res.status(500).json({ error: msg });
    else { res.write(`data: ${JSON.stringify({ error: msg })}\n\n`); res.end(); }
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
