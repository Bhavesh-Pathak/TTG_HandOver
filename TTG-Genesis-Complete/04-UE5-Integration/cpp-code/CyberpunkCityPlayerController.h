#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "CyberpunkCityPlayerController.generated.h"

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API ACyberpunkCityPlayerController : public APlayerController
{
    GENERATED_BODY()

public:
    ACyberpunkCityPlayerController();

protected:
    virtual void BeginPlay() override;
    virtual void SetupInputComponent() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Player Abilities")
    TArray<FString> PlayerAbilities;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Player Settings")
    float MovementSpeed = 5.0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Player Settings")
    float JumpHeight = 2.0;

public:
    UFUNCTION(BlueprintCallable, Category = "Player")
    bool HasAbility(const FString& AbilityName) const;

    UFUNCTION(BlueprintCallable, Category = "Player")
    void LoadPlayerSettings();
};