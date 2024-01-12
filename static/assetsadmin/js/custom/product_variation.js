

    // document.addEventListener('DOMContentLoaded', () => {
    //     const addVariantButton = document.getElementById('add-variant-button');
    //     const variantsContainer = document.getElementById('variants-container');
    //     const maxVariants = 5; // Set the maximum number of variants
    //     const maxImages = 5; // Set the maximum number of images per variant

    //     let variantCount = 1; // Initialize the variant count

    //     addVariantButton.addEventListener('click', () => {
    //         if (variantCount < maxVariants) {
    //             const newVariantDiv = document.createElement('div');
    //             newVariantDiv.classList.add('variant-container');
    //             newVariantDiv.innerHTML = `
    //                 <!-- Variant ${variantCount + 1} -->
    //                 <div class="mb-4 row gx-2">
    //                     <label class="form-label">Material</label>
    //                     <input placeholder="" type="text" class="form-control" name="variant_material" required>
    //                     <label class="form-label">Price</label>
    //                     <input placeholder="" type="text" class="form-control" name="variant_price" required>
    //                     <label class="form-label">Stock</label>
    //                     <input placeholder="" type="text" class="form-control" name="variant_stock" required>

    //                     <!-- Images for Variant ${variantCount + 1} -->
    //                     <div class="images-container" data-variant-index="${variantCount}">
    //                         <label class="form-label">Images</label>
    //                         <input class="form-control" name="images_${variantCount}_0" type="file" accept="image/*" required>
    //                     </div>
    //                     <button type="button" class="add-image-button" data-variant-index="${variantCount}">Add Image</button>
    //                 </div>
    //             `;

    //             variantsContainer.appendChild(newVariantDiv);
    //             variantCount++;
    //         } 
    //     });

    //     // Add Image button for all variants
    //     document.addEventListener('click', event => {
    //         if (event.target.classList.contains('add-image-button')) {
    //             const variantIndex = event.target.dataset.variantIndex;
    //             const imagesContainer = document.querySelector(`[data-variant-index="${variantIndex}"]`);
    //             const imageCount = imagesContainer.querySelectorAll('input[type="file"]').length;

    //             if (imageCount < maxImages) {
    //                 const newImageInput = document.createElement('input');
    //                 newImageInput.setAttribute('class', 'form-control');
    //                 newImageInput.setAttribute('type', 'file');
    //                 newImageInput.setAttribute('name', `images_${variantIndex}_${imageCount}`);
    //                 newImageInput.setAttribute('accept', 'image/*');
    //                 newImageInput.required = true;

    //                 imagesContainer.appendChild(newImageInput);
    //             }
    //         }
    //     });
    // });

    document.addEventListener('DOMContentLoaded', () => {
        const addVariantButton = document.getElementById('add-variant-button');
        const variantsContainer = document.getElementById('variants-container');
        const maxVariants = 5; // Set the maximum number of variants
        const maxImages = 5; // Set the maximum number of images per variant
    
        let variantCount = 1; // Initialize the variant count
    
        addVariantButton.addEventListener('click', () => {
            if (variantCount < maxVariants) {
                const newVariantDiv = document.createElement('div');
                newVariantDiv.classList.add('variant-container');
                newVariantDiv.innerHTML = `
                    <!-- Variant ${variantCount + 1} -->
                    <div class="mb-4 row gx-2">
                        <label class="form-label">Material</label>
                        <input placeholder="" type="text" class="form-control" name="variant_material" required>
                        <label class="form-label">Price</label>
                        <input placeholder="" type="text" class="form-control" name="variant_price" required>
                        <label class="form-label">Stock</label>
                        <input placeholder="" type="text" class="form-control" name="variant_stock" required>
                    
                        <!-- Images for Variant ${variantCount + 1} -->
                        <div class="images-container" data-variant-index="${variantCount}">
                            <label class="form-label">Images</label>
                            <input class="form-control" name="images_${variantCount}_0" type="file" accept="image/*" required>
                        </div>
                        <button type="button" class="add-image-button" data-variant-index="${variantCount}">Add Image</button>
                    </div>
                `;
    
                variantsContainer.appendChild(newVariantDiv);
                variantCount++;
            }
        });
    
        // Add Image button for all variants
        document.addEventListener('click', event => {
            if (event.target.classList.contains('add-image-button')) {
                const variantIndex = event.target.dataset.variantIndex;
                const imagesContainer = document.querySelector(`[data-variant-index="${variantIndex}"]`);
                const imageCount = imagesContainer.querySelectorAll('input[type="file"]').length;
    
                if (imageCount < maxImages) {
                    const newImageInput = document.createElement('input');
                    newImageInput.setAttribute('class', 'form-control');
                    newImageInput.setAttribute('type', 'file');
                    newImageInput.setAttribute('name', `images_${variantIndex}_${imageCount}`);
                    newImageInput.setAttribute('accept', 'image/*');
                    newImageInput.required = true;
    
                    imagesContainer.appendChild(newImageInput);
                }
            }
        });
    });
    