from PIL import Image, ImageDraw
import random


def generate_random_rainbow_image(width, height):
	# Define rainbow colors
	colors = [
	    (255, 102, 204),  # Pink
	    (255, 255, 153),  # Light Yellow
	    (153, 255, 204),  # Light Green
	    (102, 204, 255),  # Light Blue
	    (153, 102, 255),  # Purple
	    (255, 153, 51)  # Orange
	]

	# Shuffle the colors to get a random order
	random.shuffle(colors)

	# Create a new image with white background
	img = Image.new("RGB", (width, height), "white")
	draw = ImageDraw.Draw(img)

	# Draw the random rainbow
	y_start = 0
	for color in colors:
		# Randomly select the height of the stripe for the current color
		stripe_height = random.randint(height // 10, height // 4)

		# Randomly decide the start and end points horizontally for a bit of randomness
		x_start = random.randint(0, width // 8)
		x_end = random.randint(7 * width // 8, width)

		# Create random curve points for the top and bottom of the stripe
		num_points = random.randint(3, 6)
		top_points = [
		    (int(x_start + i * (x_end - x_start) / (num_points - 1)),
		     y_start + random.randint(-stripe_height // 4, stripe_height // 4))
		    for i in range(num_points)
		]
		bottom_points = [
		    (int(x_start + i * (x_end - x_start) / (num_points - 1)),
		     y_start + stripe_height +
		     random.randint(-stripe_height // 4, stripe_height // 4))
		    for i in range(num_points)
		]

		# Draw the stripe using the curve points
		draw.polygon(top_points + bottom_points[::-1], fill=color)

		y_start += stripe_height

	return img


# Generate the random rainbow image
img = generate_random_rainbow_image(32, 32)
output_filename_random = "starving.jpg"
img.save(output_filename_random)

output_filename_random
