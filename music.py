import discord
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

SONG_QUEUES = {}

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)

# ---- COMANDOS DE MÚSICA ----

@commands.command(name="play")
async def play(ctx, *, song_query: str):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Debes estar en un canal de voz.")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client

    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_channel != voice_client.channel:
        await voice_client.move_to(voice_channel)

    ydl_options = {
        "format": "bestaudio[abr<=96]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }

    query = "ytsearch1: " + song_query
    results = await search_ytdlp_async(query, ydl_options)
    tracks = results.get("entries", [])

    if not tracks:
        await ctx.send("No se encontraron resultados.")
        return

    first_track = tracks[0]
    audio_url = first_track["url"]
    title = first_track.get("title", "Sin título")

    guild_id = str(ctx.guild.id)
    if SONG_QUEUES.get(guild_id) is None:
        SONG_QUEUES[guild_id] = deque()

    SONG_QUEUES[guild_id].append((audio_url, title))

    if voice_client.is_playing() or voice_client.is_paused():
        await ctx.send(f"Añadido a la cola: **{title}**")
    else:
        await ctx.send(f"Reproduciendo ahora: **{title}**")
        await play_next_song(voice_client, guild_id, ctx.channel)

async def play_next_song(voice_client, guild_id, channel):
    if SONG_QUEUES[guild_id]:
        audio_url, title = SONG_QUEUES[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -c:a libopus -b:a 96k",
        }

        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable="bin\\ffmpeg\\ffmpeg.exe")

        def after_play(error):
            if error:
                print(f"Error playing {title}: {error}")
            asyncio.run_coroutine_threadsafe(play_next_song(voice_client, guild_id, channel), voice_client.loop)

        voice_client.play(source, after=after_play)
        asyncio.create_task(channel.send(f"Reproduciendo: **{title}**"))
    else:
        await voice_client.disconnect()
        SONG_QUEUES[guild_id] = deque()

@commands.command(name="pause")
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Pausado.")
    else:
        await ctx.send("No estoy reproduciendo nada.")

@commands.command(name="resume")
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Reanudado.")
    else:
        await ctx.send("No estoy pausado.")

@commands.command(name="skip")
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
        await ctx.send("Saltado.")
    else:
        await ctx.send("No estoy reproduciendo nada.")

@commands.command(name="stop")
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    guild_id = str(ctx.guild.id)
    if voice_client:
        if guild_id in SONG_QUEUES:
            SONG_QUEUES[guild_id].clear()
        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()
        await voice_client.disconnect()
        await ctx.send("Música detenida y desconectado.")
    else:
        await ctx.send("No estoy en ningún canal de voz.")
