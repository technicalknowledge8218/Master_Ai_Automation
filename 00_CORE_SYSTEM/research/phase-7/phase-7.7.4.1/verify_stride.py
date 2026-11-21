# Verify stride mismatch
raw_frame_size = 1920 * 1080 * 3
pix_frame_size = 2560 * 1440 * 3
print(f"FFmpeg expected rawvideo frame size (1920x1080x3): {raw_frame_size:,} bytes")
print(f"PyMuPDF rendered pixmap size (2560x1440x3):        {pix_frame_size:,} bytes")
print(f"Byte mismatch per frame:                           {pix_frame_size - raw_frame_size:,} bytes")

for f in range(10):
    start_byte = f * pix_frame_size
    ffmpeg_frame = start_byte // raw_frame_size
    byte_offset_in_ffmpeg_frame = start_byte % raw_frame_size
    line_offset = byte_offset_in_ffmpeg_frame // (1920 * 3)
    print(f"Written frame {f:2d}: byte offset {start_byte:10,d} -> FFmpeg frame {ffmpeg_frame:2d}, vertical line shift = {line_offset:4d} lines")
