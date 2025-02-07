"""
oc_plot_lines.py
Plot line charts (x: component set, y: model fit, lines: dimensions)
"""

import os

from functions.functions import (
    PlotObject,
    load_data_object,
    prep_dim_data,
    mod_fit,
    line_plot,
    line_plot_perm,
)

# --- User input
data_object_name = "data_object_clip-vit_eighty_tools.pkl"

main_path = os.path.dirname(os.path.abspath(__file__))
data_object_path = os.path.join(main_path, "results", data_object_name)

dim_data = os.path.join(
    main_path, "data/behavioural_dimensions/", "selected_dimensions.csv"
)
out_path = os.path.join(main_path, "results/line_plots/")

mod_fit_metric = "adj_r2"

fig_label = ""

show_perm = 1

model_name_dict = {
    "clip-vit": "CLIP-ViT",
    "in21k-vit": "IN-ViT",
    "in1k-resnext101": "IN-ResNeXt101",
    "in1k-vgg16": "IN-VGG16",
    "in1k-alexnet": "IN-AlexNet",
    "ecoset-vgg16": "EcoSet-VGG16",
    "ecoset-alexnet": "EcoSet-AlexNet",
}
# --- Main

if not os.path.exists(out_path):
    os.makedirs(out_path)

# Load data object, prep dims
data_object = load_data_object(data_object_path)
dim_vals, _ = prep_dim_data(dim_data, data_object.dim_names)

# Calculate model fits
mod_fit_mat = mod_fit(
    data_object.pred_mat, dim_vals, data_object.bkc_sizes, mod_fit_metric
)

# Run incremental line plots
if show_perm == 1:
    # Get mod_fit_perm_mat
    mfpm_name = f"mod_fit_perm_mat_{mod_fit_metric}"
    mod_fit_perm_mat = getattr(data_object, mfpm_name)

    # Instantiate PlotObject
    plot_object = PlotObject(
        model_name=data_object.model_name,
        dim_names=data_object.dim_names,
        mod_fit_metric=mod_fit_metric,
        mod_fit_mat=mod_fit_mat,
        mod_fit_perm_mat=mod_fit_perm_mat,
        bkc_sizes=data_object.bkc_sizes,
        out_path=out_path,
        fig_label=fig_label,
    )

    line_plot_perm(plot_object, model_name_dict)
else:
    # Instantiate PlotObject
    plot_object = PlotObject(
        model_name=data_object.model_name,
        dim_names=data_object.dim_names,
        mod_fit_metric=mod_fit_metric,
        mod_fit_mat=mod_fit_mat,
        mod_fit_perm_mat=None,
        bkc_sizes=data_object.bkc_sizes,
        out_path=out_path,
        fig_label=fig_label,
    )

    line_plot(plot_object, model_name_dict)
