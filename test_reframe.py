
from src.image_inspector import inspect_image
from src.image_reframer import reframe_image

input_path = "input/images (2).jpeg"
output_path = "output/images_vertical.png"

print("Original image:")
print(inspect_image(input_path))

print("\nCreating vertical image...")

result = reframe_image(
    input_path=input_path,
    output_path=output_path,
    target_ratio="9:16",
)

print("Reframing result:")
print(result)

print("\nOutput image:")
print(inspect_image(output_path))