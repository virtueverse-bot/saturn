import moviepy.editor as mp
import os
import random
from moviepy.video.fx.all import resize, colorx
from flask import Flask, render_template, redirect, url_for, request
from datetime import date
from openai import OpenAI

client = OpenAI()

app = Flask(__name__, static_url_path='/static')

# Set your OpenAI API key
OpenAI.api_key = os.getenv('OPENAI_API_KEY')


# Function to generate a motivational quote using ChatGPT
def generate_motivational_quote():
    # prompt = """
    # generate ONE motivational/emotional/stoic quote for an IG reel or TikTok in this theme

    # "Being in the same place as last year should terrify you. Stay focused"
    # "It won't happen overnight. But if you quit, it won't happen at all"
    # "Focus on you until the focus is on you"
    # "If only u knew how many times I stayed up at night thinking about a way to make myself better for u"  
    # "It's time for your comeback."

    # Do not make them too long, 1 or 2 sentences is enough

    # """
    
    
  
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "generate ONE motivational/emotional/stoic quote for an IG reel or TikTok in this theme\n\n    \"Being in the same place as last year should terrify you. Stay focused\"\n    \"It won't happen overnight. But if you quit, it won't happen at all\"\n    \"Focus on you until the focus is on you\"\n    \"If only u knew how many times I stayed up at night thinking about a way to make myself better for u\"  \n    \"It's time for your comeback.\"\n\n    Do not make them too long, 1 or 2 sentences is enough"
        },
        {
        "role": "user",
        "content": ""
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )


    quote = completion.choices[0].message.content.strip()
    print(quote)
    # quote = "i hate niggas"
    return quote


# Function to create a video with quote, clips, and music
def create_motivational_video(quote, clips_folder="clips", music_folder="songs", output_path="motivational_video_4.mp4"):
    # Choose an audio file from the music folder and limit it to the first 12 seconds
    music_file = random.choice(os.listdir(music_folder))
    audio_clip = mp.AudioFileClip(os.path.join(music_folder, music_file)).subclip(0, 12)

    # Choose random clips from the clips folder that cover 12 seconds in total
    clips = []
    total_duration = 0
    target_duration = 8
    print("XX")


    target_duration = 8  # Change the target duration to 8 seconds
    num_clips = 8  # Change to the number of clips you want

    while len(clips) < num_clips:
        random_clip = random.choice(os.listdir(clips_folder))
        clip_duration = 1  # Set the duration to 1 second for each clip
        if total_duration + clip_duration <= target_duration:
            clips.append((random_clip, clip_duration))
            total_duration += clip_duration

        print(clips)

    # Resize and concatenate the video clips
    resized_clips = []
    for clip in clips:
        if isinstance(clip, tuple):  # Check if it's a tuple with duration
            clip_name, duration = clip
            print(os.path.join(clips_folder, clip_name))
            path = "/app/Clips/resized_Snaptik_6988980223647747334_josh-chapman97-1.mov"
            video_clip = mp.VideoFileClip(path).subclip(0, duration)
        else:
            video_clip = mp.VideoFileClip(os.path.join(clips_folder, clip))
            print(video_clip)
            
        resized_clip = resize(video_clip, height=1920, width=1080)  # Resize to 1080x1920
        print(resized_clip)
        resized_clips.append(resized_clip)

    # Concatenate the resized video clips
    final_clip = mp.concatenate_videoclips(resized_clips, method="compose")

    # Set the duration of the final video based on the target duration
    final_duration = min(final_clip.duration, target_duration)

    # Set the audio of the final video
    final_clip = final_clip.set_audio(audio_clip.subclip(0, final_duration))

    # Add dark overlay with low opacity to the final video
    dark_overlay = colorx(final_clip, factor=0.65)  # Adjust factor for opacity

          # Split quote into lines without breaking words
    max_chars_per_line = 35  # Adjust this based on your preference
    words = quote.split()
    lines = []
    current_line = ""
    print("here")
    for word in words:
        if len(current_line + word) <= max_chars_per_line:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:  # Add the last line if not empty
        lines.append(current_line.strip())

    # Dynamically adjust font size based on quote length
    max_font_size = 32  # Adjust this based on your preference
    font_size = min(max_font_size, int(1920 / len(lines)))  # Ensure font size doesn't exceed screen height

    print(mp.TextClip.list('font'))
    # Add text with the motivational quote to the final video
    txt_clip = mp.TextClip('\n'.join(lines), fontsize=font_size, color='white', font='Ariel')
    txt_clip = txt_clip.set_pos('center').set_duration(final_duration)
    final_clip = mp.CompositeVideoClip([dark_overlay, txt_clip])
    # Resize the final video to have dimensions 1080x1920
    final_clip = final_clip.resize(height=1920, width=1080)

    # Write the final video to a file
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')



# i = 40
# while i < 55:
#     # Generate a motivational quote
#     motivational_quote = generate_motivational_quote()
#     # Create a motivational video with the generated quote, clips, and music
#     create_motivational_video(motivational_quote, output_path=f"video{i}.mp4")
#     i += 1

@app.route('/')
def hello():
    today_date = date.today()
    formatted_date = today_date.strftime("%Y-%m-%d")
    morning_quote = request.args.get('morning_quote')
    evening_quote = request.args.get('evening_quote')


    return render_template('index.html', morning_video=f"morning_{formatted_date}.mp4", evening_video=f"evening_{formatted_date}.mp4", morning_quote=morning_quote, evening_quote = evening_quote)

@app.route('/generate')
def generate():
    
    
    print("REQUEST TO GENERATE")

    policy_line = '<policy domain="module" rights="read|write" pattern="{PS,PDF,XPS}" />'
    file_path = '/etc/ImageMagick-6/policy.xml'

    try:
        with open(file_path, 'a') as file:
            file.write(policy_line + '\n')
        print(f"Line added to {file_path}")
    except Exception as e:
        print(f"Error: {e}")


    today_date = date.today()
    formatted_date = today_date.strftime("%Y-%m-%d")
    # Generate quotes and create videos
    morning_quote = generate_motivational_quote()
    evening_quote = generate_motivational_quote()

    clips_folder_path = "/app/Clips/" 
    # os.path.join(os.getcwd(), 'Clips')
    music_folder_path = "/app/songs/" 
    # os.path.join(os.getcwd(), 'songs')
    create_motivational_video(morning_quote, output_path=f"static/morning_{formatted_date}.mp4", clips_folder=clips_folder_path, music_folder=music_folder_path)
    create_motivational_video(evening_quote, output_path=f"static/evening_{formatted_date}.mp4", clips_folder=clips_folder_path, music_folder=music_folder_path)
    print(f"Static URL Path: {app.static_url_path}")


    # redirect a home e passa le quotes.
    return redirect(url_for('hello', morning_quote=morning_quote, evening_quote=evening_quote))
    #return "done"




if __name__ == '__main__':
    app.run(debug=True)