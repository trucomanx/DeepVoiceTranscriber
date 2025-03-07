# deep-voice-transcriber

Program that improves text writing

## Testar indicator

```bash
cd src
python3 -m deep_voice_transcriber.indicator
```

## Upload to PYPI

```bash
cd src
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Install from PYPI

The homepage in pipy is https://pypi.org/project/deep-voice-transcriber/

```bash
pip install --upgrade deep-voice-transcriber
```

Using:

```bash
deep-voice-transcriber-indicator
```

## Install from source
Installing `deep-voice-transcriber` program

```bash
git clone https://github.com/trucomanx/ClipboardTextCorrection.git
cd ClipboardTextCorrection
pip install -r requirements.txt
cd src
python3 setup.py sdist
pip install dist/deep_voice_transcriber-*.tar.gz
```
Using:

```bash
deep-voice-transcriber-indicator
```

## Uninstall

```bash
pip uninstall deep_voice_transcriber
```
