import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import { existsSync } from 'fs'
import { join } from 'path'

export async function POST(request: Request) {
  try {
    const { plot } = await request.json()

    const scriptPath = join(process.cwd(), 'movie_genre_prediction.py')
    
    if (!existsSync(scriptPath)) {
      console.error('Python script not found:', scriptPath)
      return NextResponse.json({ error: 'Internal server error: Python script not found' }, { status: 500 })
    }

    return new Promise((resolve) => {
      const python = spawn('python', [scriptPath, plot])

      let dataToSend = ''
      let errorData = ''

      python.stdout.on('data', (data) => {
        dataToSend += data.toString()
      })

      python.stderr.on('data', (data) => {
        errorData += data.toString()
      })

      python.on('close', (code) => {
        console.log(`Python script exited with code ${code}`)
        if (code !== 0) {
          console.error('Python script error:', errorData)
          resolve(NextResponse.json({ error: 'Failed to predict genres: ' + errorData }, { status: 500 }))
        } else {
          const genres = dataToSend.trim().split(',')
          resolve(NextResponse.json({ genres }))
        }
      })
    })
  } catch (error) {
    console.error('API route error:', error)
    return NextResponse.json({ error: 'Internal server error: ' + (error instanceof Error ? error.message : String(error)) }, { status: 500 })
  }
}

