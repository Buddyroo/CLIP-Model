image_features = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
text_features = torch.tensor([[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]])

image_features:
tensor([[1., 2., 3.],
        [4., 5., 6.]])
text_features:
tensor([[ 7.,  8.,  9.],
        [10., 11., 12.]])


combined_features:
tensor([[ 1.,  2.,  3.],
        [ 4.,  5.,  6.],
        [ 7.,  8.,  9.],
        [10., 11., 12.]])

mean_features = combined_features.mean(dim=0, keepdim=True)


mean_features:
tensor([[5.5, 6.5, 7.5]])