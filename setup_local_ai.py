"""Download pinned official runtime/model; verify published SHA-256 hashes."""
import hashlib, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent
DEST = ROOT / 'runtime'
DEST.mkdir(exist_ok=True)
FILES = [
 ('Qwen3-0.6B-Q8_0.gguf', 'https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/resolve/23749fefcc72300e3a2ad315e1317431b06b590a/Qwen3-0.6B-Q8_0.gguf', '9465e63a22add5354d9bb4b99e90117043c7124007664907259bd16d043bb031'),
 ('Qwen-LICENSE.txt', 'https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/resolve/23749fefcc72300e3a2ad315e1317431b06b590a/LICENSE', None),
]
for name, url, expected in FILES:
    path = DEST / name
    if not path.exists():
        print('Downloading', name, flush=True)
        tmp = path.with_suffix('.partial')
        req = urllib.request.Request(url, headers={'User-Agent':'ClientDesk-Local-Installer/1.0'})
        with urllib.request.urlopen(req, timeout=60) as response, tmp.open('wb') as out:
            total = 0
            while block := response.read(1024*1024):
                out.write(block)
                total += len(block)
                if total % (50*1024*1024) == 0:
                    print(f'{name}: {total//1024//1024} MB', flush=True)
        tmp.replace(path)
    if expected:
        digest = hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()
        if digest != expected:
            raise RuntimeError(f'Checksum mismatch: {name}')
        print('Verified', name, flush=True)
(DEST / 'sources.json').write_text(json.dumps(FILES, indent=2), encoding='utf-8')
print('Local AI installed.', flush=True)
