import discord
from discord.ext import commands
import requests
import os
import json
from music import play, pause, resume, skip, stop  # Mantiene tu mÃ³dulo de mÃºsica de fÃ¡brica

# Token real cargado directamente
token = "token secreto de discord"

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

# REGISTRO DE COMANDOS DE MÃšSICA
bot.add_command(play)
bot.add_command(pause)
bot.add_command(resume)
bot.add_command(skip)
bot.add_command(stop)

AGENDA_FILE = "agenda.json"

def cargar_agenda():
    if os.path.exists(AGENDA_FILE):
        with open(AGENDA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_agenda(agenda):
    with open(AGENDA_FILE, "w", encoding="utf-8") as f:
        json.dump(agenda, f, ensure_ascii=False, indent=4)

# ---- COMANDOS DE LA AGENDA ----

@bot.command()
async def tarea_add(ctx, *, tarea: str):
    """Agrega una tarea o evento pendiente"""
    agenda = cargar_agenda()
    user_id = str(ctx.author.id)
    
    if user_id not in agenda:
        agenda[user_id] = []
        
    agenda[user_id].append(tarea)
    guardar_agenda(agenda)
    
    embed = discord.Embed(title="ðŸ“ AGENDA ACTUALIZADA", description=f"ðŸ“‹ Tarea registrada con Ã©xito:\n`{tarea}`", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def agenda(ctx):
    """Muestra tus pendientes registrados"""
    agenda = cargar_agenda()
    user_id = str(ctx.author.id)
    
    embed = discord.Embed(title="ðŸ“… TU AGENDA PERSONAL", color=discord.Color.blue())
    
    if user_id in agenda and agenda[user_id]:
        lista_tareas = ""
        for i, tarea in enumerate(agenda[user_id], 1):
            lista_tareas += f"**{i}.** {tarea}\n"
        embed.description = lista_tareas
    else:
        embed.description = "âŒ No tienes eventos o tareas pendientes en este momento."
        
    await ctx.send(embed=embed)

@bot.command()
async def tarea_del(ctx, numero: int):
    """Elimina una tarea por su nÃºmero de lista"""
    agenda = cargar_agenda()
    user_id = str(ctx.author.id)
    
    if user_id in agenda and 0 < numero <= len(agenda[user_id]):
        tarea_eliminada = agenda[user_id].pop(numero - 1)
        guardar_agenda(agenda)
        embed = discord.Embed(title="ðŸ—‘ï¸ TAREA ELIMINADA", description=f"Se quitÃ³ de la lista:\n`{tarea_eliminada}`", color=discord.Color.orange())
        await ctx.send(embed=embed)
    else:
        await ctx.send("âš ï¸ **Error:** NÃºmero de tarea no vÃ¡lido o lista vacÃ­a.")

# ---- COMANDO DE CLIMA ----

@bot.command()
async def clima(ctx, *, ciudad: str):
    """Muestra el clima actual de cualquier ciudad en espaÃ±ol"""
    try:
        # Se agrega &lang=es para forzar el idioma espaÃ±ol en la respuesta de la API
        url = f"https://wttr.in/{ciudad}?format=j1&lang=es"
        response = requests.get(url).json()
        
        current = response['current_condition'][0]
        temp = current['temp_C']
        
        # Intenta buscar la descripciÃ³n traducida, si no usa la de defecto
        desc = current['lang_es'][0]['value'] if 'lang_es' in current else current['weatherDesc'][0]['value']
        humedad = current['humidity']
        
        embed = discord.Embed(title=f"ðŸŒ¤ï¸ REPORTE METEOROLÃ“GICO: {ciudad.upper()}", color=discord.Color.gold())
        embed.add_field(name="ðŸŒ¡ï¸ Temperatura:", value=f"`{temp}Â°C`", inline=True)
        embed.add_field(name="ðŸ’§ Humedad:", value=f"`{humedad}%`", inline=True)
        embed.add_field(name="ðŸ“Š Estado:", value=f"`{desc}`", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error clima: {e}")
        await ctx.send("âŒ **Error:** No se pudo obtener el clima para esa localizaciÃ³n. Verifica el nombre.")

# ---- PANEL DE AYUDA ----

@bot.command()
async def info(ctx):
    """Despliega el menÃº del sistema"""
    embed = discord.Embed(title="âš™ï¸ SISTEMA CENTRAL - LABORATORIO DE IA", color=discord.Color.purple())
    
    embed.add_field(name="ðŸŽµ MULTIMEDIA", value="`$play <bÃºsqueda/url>` | `$pause` | `$resume` | `$skip` | `$stop`", inline=False)
    embed.add_field(name="ðŸ“… AGENDA PERSONAL", value="`$tarea_add <texto>` - AÃ±adir pendiente\n`$agenda` - Ver tu lista de tareas\n`$tarea_del <nÃºmero>` - Borrar tarea realizada", inline=False)
    embed.add_field(name="ðŸŒ¤ï¸ MÃ“DULO AMBIENTAL", value="`$clima <ciudad>` - Consulta el tiempo actual", inline=False)
    
    embed.set_footer(text="Usa el prefijo $ antes de cada comando.")
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"ðŸ–¥ï¸ [LOG] {message.channel} -> {message.author.name}: {message.content}")
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"==========================================")
    print(f" Â¡Estamos dentro! MÃ³dulos cargados con Ã©xito.")
    print(f"ðŸ›°ï¸ CONECTADO COMO: {bot.user}")
    print(f"==========================================")

bot.run(token)
