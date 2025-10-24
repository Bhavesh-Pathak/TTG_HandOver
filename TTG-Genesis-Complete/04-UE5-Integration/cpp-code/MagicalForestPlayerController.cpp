#include "MagicalForestPlayerController.h"
#include "Engine/Engine.h"

AMagicalForestPlayerController::AMagicalForestPlayerController()
{
    // Initialize player abilities
        PlayerAbilities.Add(TEXT("walk"));
    PlayerAbilities.Add(TEXT("run"));
    PlayerAbilities.Add(TEXT("jump"));
    PlayerAbilities.Add(TEXT("interact"));
    PlayerAbilities.Add(TEXT("cast_spells"));
}

void AMagicalForestPlayerController::BeginPlay()
{
    Super::BeginPlay();
    LoadPlayerSettings();
}

void AMagicalForestPlayerController::SetupInputComponent()
{
    Super::SetupInputComponent();
    // Setup input bindings here
}

bool AMagicalForestPlayerController::HasAbility(const FString& AbilityName) const
{
    return PlayerAbilities.Contains(AbilityName);
}

void AMagicalForestPlayerController::LoadPlayerSettings()
{
    UE_LOG(LogTemp, Warning, TEXT("Loaded player settings - Speed: %f, Jump: %f"), MovementSpeed, JumpHeight);
}