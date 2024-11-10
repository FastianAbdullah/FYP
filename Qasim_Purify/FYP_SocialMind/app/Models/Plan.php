<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Plan extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        // Add other fields that your plans table has
    ];

    /**
     * Get the users for the plan.
     */
    public function users()
    {
        return $this->hasMany(User::class);
    }
}