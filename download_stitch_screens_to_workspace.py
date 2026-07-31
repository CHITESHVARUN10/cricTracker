import os
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

screens_data = [
    {"id": "e2e044a31c494326bfcbce30272e4830", "title": "01_shell", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYTE5MGRlNTAwMDMwMTE5NzdmMTE5MWNkEgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLtb4MTmwNGgGA5AnJaELKExbU4UFe-I3eHXj3BXHormiAMopKDh1Ap3T9VTutK2voMvEHFxISYdpPU1PiN2SgYwRf9hetF3-e5SbX7ikZjnJEM71hmNJ5_BSsnY0hQ7-KMjLZfmSksIjJMzwY6pjWs7C60ByD8Lt5UhM9s5FHSTxdZRmAH14oDhx07wW4Kr8oKGGiD-ep325IbWzIv_czbWuTY9_kHUjJ3YBhHShALhdzS5wjTbLJnzz_E_"},
    {"id": "bb3894a20fa84c07ac3f87bea51c58b2", "title": "02_overview", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYTM1YTQwMTEwMzgzOTkwZmExMTlmNzI1EgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLsrACgaZ9rTx-VBJbCirAZ6tK0Oeqf_UEcHDyKbD6BuguDGtB9unl-Yqp_OXw3FoX1Wt7m8cle_8e5SEomQ3pTq3yLrW6bvI0CLsW2Sj0o-tTYKvl0aAjHOCBxPkTtmV3K_CSwHayWZPRpy196tFybuQbpvOwvZMJzN2YGsWKW5F2ZCvkHDvic6l6CnrhuwtEjxRiENjkGPWHg9s_DtglHCEXSJZcwpE2GLMImlJMfb7gZsBFvBP_fxCl2R"},
    {"id": "d9fdacc1d7b247a8ab948333d576636d", "title": "03_toss", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYTI5OGNlNjcwNWMyYzc3ZDhmMGQ1NzllEgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLvor-HChrVZr3Fs3FAOAp8h86m7Qnm_UvgNZnt8AkbqY32b8MyfQX1nGaDvjUJuRc2wixoYNAL0cY9PK4VmXrqanGI8W5ajFdcx5ATFafP2qqGOLDFWTr0PS6PJ5wQykfqsuOH5nBf9Lo5C9tau4Wae7Hc9x3cmdyJytKxani1t932AII8s2Dkg0BcXI5kVql_IJD-YwLn34CtZZFEVVvT1CtpE3nAOy6DnNfzYeQd8WYFHZPyt1JJBKr8"},
    {"id": "67c242991dc440c39b5b87151f0dcf45", "title": "04_venue", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYTNiYjIyYzkwN2M0ZWQ0M2QwMzVjMTcxEgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLuKkPioCpq8T_ziw_Tx7eqWtY2BfWtrsz7o-KvsNeYl7gchoj1gjudNna0fSn3CKCU2ljNcckXGlBglP5QY5qPXfexfLcARMbnhesVdHDXFcr3Pw47Jhh3gQZewav47QOy5SjS22W2__TPwnA6iRoH7aryqXvz1uX7NGUcbYsDxPsmAY79uCj2kldPMolGifYJyr_CwUImmI3SV725OS1i03cfH6Xc-IXjeoNBGbVIJaHXcTKyREgrNqVoR"},
    {"id": "c13fd63f85214eeabc2726e44b19d3fb", "title": "05_teams", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYTU0MDcwZmMwMmE5YTM0MmRmMzhlYTBmEgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLv3xnOqvGvnzxQpWQ0K8Q7YZ7Xy7xQ0cKgqFlvwRN-hOAH6Fwu5oBiv_ebvg1WBkcWTm0poiDDzPFVHukZIpE40eieldw1RU4yEZHwIR16GmuHtAPOcaEYYkOP1-0C3q9mZ3Xj3Kkat-_0SGWO62A0aVuPiIE-F5AfWuyJzDmkk2_iAw-cZ27fB8FMY32Xwt4A78bmzFQUZtTLJy0bSZiOGneB0PiCREPHFunqLmlrALARIMrptPw4YoY0"},
    {"id": "3b4e29a57c194080a910b8619537674a", "title": "06_players", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYWNlNDc2MGIwMWE2MDNlOGYyMTliZGI1EgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLvrkKi0J46jcT8J4o3BnQbWo5GBqvI6kkPYn7U6j04jX_spyBXqvbJHMwVpTAqvuYMrJTpnRggsh9lKFuMikX7bA3ZyRJEZ0URljZ0e7vFDqhQn1td3rcjTvl4pMQ4sbDzPz0OceKCZKcx-3rfln7eeCf4ZNZWPK6D8FHB7IRSaLBRKgMfHKKzeCnZEczkKP3dnooDHMuUxR2FDkYosE2uD-A512j-I3PtuU6E05S-FToytK8HBFzh6c7qs"},
    {"id": "cf1cbb1f191d45feb195d4a3902ea70a", "title": "07_insights_lab", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYjI5NjMyZDYwMmE5YjQwYWRhMDhmMmY5EgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLuBZX22zU9ynIxYJcddxKSAe_DTKmUSxIXUrC8lQleLTF0w43gseUH5Q5e2aldNxhe3msYhh6nduvBsq8TEmd8w0RtJXc_V_O2njv0WU0m14CgW90bi5QgG8z0j3UFGEVV0aZzU7ltejfEw3PF2NEO0DryXmwE-wU97KfR1S6ZRcZmBfbZFjkTKT168bWhrC4V2Bv9vZduboHWrC3wPjRfPFjOj4Sc-8RdHBPw0v5TObeUeIr3UiyJQFokr"},
    {"id": "20339d46a57648aeae05c35413a82d4a", "title": "08_phases", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYjY2OTFjZDQwODE2ZmUwYWFiMTNjY2E4EgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLuAU8jLVeIAciuaR2qxmlr8scsloEDDd-VMUuVbqlud_mt1Cxnd0E65O1QV9uQ9PGAu8daHQ5V_nLGggJYHfrIVc9DRPP2VoyynwQI3NicpJh-uofm-uVoRAhTel41Mwd3oYB3GEwzPuByxjZ8mO5Aj3IcnEdfLp7kwdd5gNQbY60p9ps-MevKiRDoIt7v5PpWL30FUrKuLXTXVIROrCSWBiRRtCbRdKTn4YS0nv-LnBxlgAatONQJZMJDV"},
    {"id": "ec62b793f5164157876eb9959cbf61c9", "title": "09_matchups", "html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ8Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpbCiVodG1sXzAwMDY1NjNkYjZkZmNjYjQwMmE5YjQwYWRhMDhmMmY5EgsSBxCc8aXemRoYAZIBJAoKcHJvamVjdF9pZBIWQhQxMDUwMDU0MzIwOTkwMjM5MjU5MA&filename=&opi=89354086", "img": "https://lh3.googleusercontent.com/aida/AP1WRLt8oINb2wSCmHtBi7d1ACnn2gY5x_cZMda5dx7ulC5utPlUyXEKGcsmrvFf-YoH2kp4XsFRQ02xyzahMp7C8DHK-Myswr5EcTLCNQ4uHjtWtDn7Agp7tlTHlF8-4ABFsduWfWuOlyK5mh_Wbw14abrhliveUT86bJThFL1RC6RuW4ChRITYAOScQMa42hbOJJPKjRq9vsF6slzDOV7e1vxRDKR0BVqYzUM8hGhZfFx1E3FGzZzQqQE2lNPu"}
]

out_dirs = [
    "/Users/chiteshvarun/D-drive/crictrack/stitch_screens",
    "/Users/chiteshvarun/D-drive/crictrack/cricTracker/stitch_screens"
]

for out_dir in out_dirs:
    os.makedirs(out_dir, exist_ok=True)
    for item in screens_data:
        html_path = os.path.join(out_dir, f"{item['title']}.html")
        png_path = os.path.join(out_dir, f"{item['title']}.png")
        
        print(f"Downloading {item['title']} to {os.path.basename(out_dir)}...")
        try:
            req_html = urllib.request.Request(item['html'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_html, context=ctx) as response, open(html_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f" Saved HTML ({os.path.getsize(html_path)} bytes)")
        except Exception as e:
            print(f" Error HTML {item['title']}: {e}")
            
        try:
            req_img = urllib.request.Request(item['img'], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img, context=ctx) as response, open(png_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f" Saved PNG ({os.path.getsize(png_path)} bytes)")
        except Exception as e:
            print(f" Error PNG {item['title']}: {e}")

print("Successfully downloaded all HTML and PNG screens into stitch_screens folders.")
