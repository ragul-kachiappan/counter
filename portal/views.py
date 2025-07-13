from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction, models
from .models import Cube, Tree


# Cube Views
def home(request):
    """Display all cubes with CRUD operations"""
    cubes = Cube.objects.all()
    return render(request, 'cubes/home.html', {'cubes': cubes})


def cube_create(request):
    """Create a new cube with specified number of trees"""
    if request.method == 'POST':
        name = request.POST.get('name')
        number_of_trees = int(request.POST.get('number_of_trees', 0))
        
        if name and number_of_trees > 0:
            with transaction.atomic():
                cube = Cube.objects.create(name=name, number_of_trees=number_of_trees)
                
                # Create trees for the cube
                trees_to_create = []
                for i in range(1, number_of_trees + 1):
                    trees_to_create.append(Tree(cube=cube, tree_id=i))
                Tree.objects.bulk_create(trees_to_create)
                
            messages.success(request, f'Cube "{name}" created with {number_of_trees} trees.')
            return redirect('cubes:home')
        else:
            messages.error(request, 'Please provide valid name and number of trees.')
    
    return render(request, 'cubes/cube_form.html', {'action': 'Create'})


def cube_detail(request, cube_id):
    """Display cube details and its trees"""
    cube = get_object_or_404(Cube, id=cube_id)
    trees = cube.trees.all()
    
    # Get status counts for summary
    status_counts = {}
    for choice_value, choice_label in Tree.STATUS_CHOICES:
        status_counts[choice_label] = trees.filter(status=choice_value).count()
    
    return render(request, 'cubes/cube_detail.html', {
        'cube': cube,
        'trees': trees,
        'status_counts': status_counts,
        'tree_status_choices': Tree.STATUS_CHOICES
    })


def cube_update(request, cube_id):
    """Update cube details"""
    cube = get_object_or_404(Cube, id=cube_id)
    
    if request.method == 'POST':
        cube.name = request.POST.get('name', cube.name)
        cube.save()
        messages.success(request, f'Cube "{cube.name}" updated successfully.')
        return redirect('cubes:cube_detail', cube_id=cube.id)
    
    return render(request, 'cubes/cube_form.html', {'cube': cube, 'action': 'Update'})


def cube_delete(request, cube_id):
    """Delete a cube and all its trees"""
    cube = get_object_or_404(Cube, id=cube_id)
    
    if request.method == 'POST':
        cube_name = cube.name
        cube.delete()
        messages.success(request, f'Cube "{cube_name}" deleted successfully.')
        return redirect('cubes:home')
    
    return render(request, 'cubes/cube_confirm_delete.html', {'cube': cube})


def cube_adjust_trees(request, cube_id):
    """Increase or decrease tree count within a cube"""
    cube = get_object_or_404(Cube, id=cube_id)
    
    if request.method == 'POST':
        new_count = int(request.POST.get('new_count', cube.number_of_trees))
        current_count = cube.trees.count()
        
        with transaction.atomic():
            if new_count > current_count:
                # Add trees
                trees_to_create = []
                max_tree_id = cube.trees.aggregate(max_id=models.Max('tree_id'))['max_id'] or 0
                for i in range(current_count + 1, new_count + 1):
                    trees_to_create.append(Tree(cube=cube, tree_id=max_tree_id + i - current_count))
                Tree.objects.bulk_create(trees_to_create)
                
            elif new_count < current_count:
                # Remove trees (remove from the end)
                trees_to_remove = cube.trees.order_by('-tree_id')[:current_count - new_count]
                tree_ids_to_remove = [tree.id for tree in trees_to_remove]
                Tree.objects.filter(id__in=tree_ids_to_remove).delete()
            
            cube.number_of_trees = new_count
            cube.save()
            
        messages.success(request, f'Tree count adjusted to {new_count}.')
        return redirect('cubes:cube_detail', cube_id=cube.id)
    
    return render(request, 'cubes/cube_adjust_trees.html', {'cube': cube})


# Tree Views
def tree_list(request, cube_id):
    """List all trees for a specific cube"""
    cube = get_object_or_404(Cube, id=cube_id)
    trees = cube.trees.all()
    return render(request, 'cubes/tree_list.html', {'cube': cube, 'trees': trees})


def tree_create(request, cube_id):
    """Create a new tree within a cube"""
    cube = get_object_or_404(Cube, id=cube_id)
    
    if request.method == 'POST':
        # Get next tree_id
        max_tree_id = cube.trees.aggregate(max_id=models.Max('tree_id'))['max_id'] or 0
        new_tree_id = max_tree_id + 1
        
        tree = Tree.objects.create(
            cube=cube,
            tree_id=new_tree_id,
            status=int(request.POST.get('status', 0))
        )
        
        cube.number_of_trees += 1
        cube.save()
        
        messages.success(request, f'Tree {tree.representative_name} created successfully.')
        return redirect('cubes:cube_detail', cube_id=cube.id)
    
    return render(request, 'cubes/tree_form.html', {
        'cube': cube,
        'action': 'Create',
        'status_choices': Tree.STATUS_CHOICES
    })


def tree_detail(request, tree_id):
    """Display tree details"""
    tree = get_object_or_404(Tree, id=tree_id)
    return render(request, 'cubes/tree_detail.html', {'tree': tree})


def tree_update(request, tree_id):
    """Update tree status and other details"""
    tree = get_object_or_404(Tree, id=tree_id)
    
    if request.method == 'POST':
        tree.status = int(request.POST.get('status', tree.status))
        tree.save()
        messages.success(request, f'{tree.representative_name} updated successfully.')
        return redirect('cubes:cube_detail', cube_id=tree.cube.id)
    
    return render(request, 'cubes/tree_form.html', {
        'tree': tree,
        'cube': tree.cube,
        'action': 'Update',
        'status_choices': Tree.STATUS_CHOICES
    })


def tree_delete(request, tree_id):
    """Delete a specific tree"""
    tree = get_object_or_404(Tree, id=tree_id)
    cube = tree.cube
    
    if request.method == 'POST':
        tree_name = tree.representative_name
        tree.delete()
        
        # Update cube tree count
        cube.number_of_trees = cube.trees.count()
        cube.save()
        
        messages.success(request, f'{tree_name} deleted successfully.')
        return redirect('cubes:cube_detail', cube_id=cube.id)
    
    return render(request, 'cubes/tree_confirm_delete.html', {'tree': tree})


def tree_bulk_update(request, cube_id):
    """Bulk update tree statuses"""
    cube = get_object_or_404(Cube, id=cube_id)
    trees = cube.trees.all()
    
    if request.method == 'POST':
        updated_count = 0
        for tree in trees:
            new_status = request.POST.get(f'status_{tree.id}')
            if new_status is not None:
                tree.status = int(new_status)
                tree.save()
                updated_count += 1
        
        messages.success(request, f'{updated_count} trees updated successfully.')
        return redirect('cubes:cube_detail', cube_id=cube.id)
    
    return render(request, 'cubes/tree_bulk_update.html', {
        'cube': cube,
        'trees': trees,
        'status_choices': Tree.STATUS_CHOICES
    })


def tree_update_status_ajax(request, tree_id):
    """AJAX endpoint to update tree status quickly"""
    if request.method == 'POST':
        tree = get_object_or_404(Tree, id=tree_id)
        new_status = int(request.POST.get('status', tree.status))
        
        if new_status in [choice[0] for choice in Tree.STATUS_CHOICES]:
            tree.status = new_status
            tree.save()
            
            return JsonResponse({
                'success': True,
                'status': tree.status,
                'status_display': tree.status_display,
                'tree_id': tree.id,
                'representative_name': tree.representative_name
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
