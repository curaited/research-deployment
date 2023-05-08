document.getElementById('generate-btn').addEventListener('click', async () => {
  console.log('Generate button clicked');
  const roomType = document.getElementById('room_type').value;
  const style = document.getElementById('style').value;
  const useRandomImage = document.getElementById('random-toggle').checked;

  const response = await fetch('/generate-image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      tags: [roomType, style],
      use_random_image: useRandomImage,
    }),
  });

  if (response.ok) {
    const data = await response.json();
    const imageUrl = data.image_url;
    document.getElementById('generated-image').src = imageUrl;
  } else {
    console.error('Error generating image');
  }
});
