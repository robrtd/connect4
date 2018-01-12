from lime import lime_image

explainer = lime_image.LimeImageExplainer()

explanation = explainer.explain_instance(image, predict_fn, top_levels=5, hide_color = 0, num_samples=1000)
tmp, mask = explainer.get_image_and_mask(x, positive_only=True, num_features=5, hide_rest=True)