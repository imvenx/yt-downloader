# /// script
# dependencies = [
#   "youtube-transcript-api",
# ]
# ///

from youtube_transcript_api import YouTubeTranscriptApi
import json
import os

# Configuration
TEXT_ONLY = True  # Set to False to include start/duration timestamps
SEPARATE_FILES = False  # Set to False to save all transcripts in one JSON file

# List of video IDs to download
video_ids = [
    'K2Lwi591jp8',
    'dQw4w9WgXcQ',
    'jNQXAC9IVRw',
    # Add more video IDs here...
]

try:
    ytt_api = YouTubeTranscriptApi()
    
    print(f"Starting bulk download of {len(video_ids)} videos...\n")
    
    all_transcripts = {}  # For storing all transcripts if SEPARATE_FILES is False
    
    if SEPARATE_FILES:
        # Create transcripts directory if it doesn't exist
        os.makedirs('transcripts', exist_ok=True)
    
    for i, video_id in enumerate(video_ids, 1):
        try:
            print(f"[{i}/{len(video_ids)}] Fetching transcript for {video_id}...")
            transcript = ytt_api.fetch(video_id)
            
            if TEXT_ONLY:
                # Just extract the text
                transcript_data = {
                    "video_id": transcript.video_id,
                    "language": transcript.language,
                    "text": " ".join(snippet.text for snippet in transcript.snippets)
                }
            else:
                # Full data with timestamps
                transcript_data = {
                    "video_id": transcript.video_id,
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "snippets": [
                        {
                            "text": snippet.text,
                            "start": snippet.start,
                            "duration": snippet.duration
                        }
                        for snippet in transcript.snippets
                    ]
                }
            
            if SEPARATE_FILES:
                # Save to individual file
                output_path = f'transcripts/{video_id}.json'
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(transcript_data, f, indent=2, ensure_ascii=False)
                print(f"  ✓ Saved to {output_path}")
            else:
                # Add to collection
                all_transcripts[video_id] = transcript_data
                print(f"  ✓ Added to collection")
            
        except Exception as e:
            print(f"  ✗ Error with {video_id}: {e}")
            if not SEPARATE_FILES:
                all_transcripts[video_id] = {"error": str(e)}
    
    # If all in one file, save it now
    if not SEPARATE_FILES:
        with open('all_transcripts.json', 'w', encoding='utf-8') as f:
            json.dump(all_transcripts, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved all transcripts to all_transcripts.json")
    
    print(f"\n✓ Done! Processed {len(video_ids)} videos")
        
except Exception as e:
    print(f"✗ Fatal error: {type(e).__name__}")
    print(f"Error message: {e}")
    import traceback
    traceback.print_exc()