Arseny
Chebyshev, [6 / 11 / 2024 3: 02
PM]
это
лучше
делать
на
стороне
инференса, при
помощи
torch.
Ну
вот
что - то
такое:


async def encode(request: EncodeRequest):
    if video_url:
        images = create_thumbnails_for_video_message(video_url)
        image_inputs = []
        for image in images:
            image = Image.open(image.file)
            image_input = processor(images=image, return_tensors="pt")
            image_inputs.append(image_input)
        with torch.no_grad():
            image_features = clip_model.get_image_features(**image_inputs[0])
            for image_input in image_inputs[1:]:
                image_feature = clip_model.get_image_features(**image_input)
                image_features = torch.cat((image_features, image_feature), dim=0)
            # Объединим все векторы изображений в средний
            features = torch.mean(image_features, dim=0)

            features /= features.norm(dim=-1, keepdim=True)


return {"features": features.tolist()}
У
torch.mean
следующая
дока:


def mean(input: Tensor, *, dtype: Optional[_dtype] = None) -> Tensor:
    r"""
    mean(input, *, dtype=None) -> Tensor

    Returns the mean value of all elements in the :attr:`input` tensor. Input must be floating point or complex.

    Args:
        input (Tensor):
          the input tensor, either of floating point or complex dtype

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
            If specified, the input tensor is casted to :attr:`dtype` before the operation
            is performed. This is useful for preventing data type overflows. Default: None.

    Example::

        >>> a = torch.randn(1, 3)
        >>> a
        tensor([[ 0.2294, -0.5481,  1.3288]])
        >>> torch.mean(a)
        tensor(0.3367)

Arseny Chebyshev, [6/11/2024 3:03 PM]
вот такая строчка позволит получить среднее между кадрами
