# tensorrt_flashcard
A simple flashcard generating app

INSTRUCTIONS:

1: Follow instructions to install TensorRT.  https://github.com/rajeevsrao/TensorRT/tree/release/9.2/demo/Diffusion.  Check your installed version using: python3 -c 'import tensorrt;print(tensorrt.__version__)'.  Uses demo_txt2img.py directly

2: git clone https://github.com/gurungh/tensorrt_flashcard.git. stable_diffusion_pipeline.py and utilities.py modified only to change the image output file names

3: pip install -r requirements.txt

4: python gui.py - To select features and generate flashcards.  Requires the environment variable OPENAI_API_KEY to be set with an active account

5: python display_flashcards.py - To display the generated flashcards
