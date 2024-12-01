import { NextResponse } from 'next/server'
import { spawn } from 'child_process'

export async function POST(request: Request) {
  const { plot } = await request.json()

  return new Promise((resolve) => {
    const python = spawn('python', ['movie_genre_prediction.py', plot])

    let dataToSend = ''
    python.stdout.on('data', function (data) {
      dataToSend += data.toString()
    })

    python.on('close', (code) => {
      console.log(`child process close all stdio with code ${code}`)
      const genres = dataToSend.trim().split(',')
      resolve(NextResponse.json({ genres }))
    })
  })
}

