#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MagicalForestEnvironment.generated.h"

USTRUCT(BlueprintType)
struct FMagicalForestEnvironmentData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString EnvironmentType = TEXT("forest");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Setting = TEXT("A lush woodland area with ancient ruins and artifacts infused with magical energy");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Lighting = TEXT("dynamic_lighting");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Weather = TEXT("clear");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FString Atmosphere = TEXT("magical");
};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API AMagicalForestEnvironment : public AActor
{
    GENERATED_BODY()

public:
    AMagicalForestEnvironment();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Environment")
    FMagicalForestEnvironmentData EnvironmentData;

public:
    UFUNCTION(BlueprintCallable, Category = "Environment")
    void LoadEnvironmentFromJSON();

    UFUNCTION(BlueprintCallable, Category = "Environment")
    void ApplyEnvironmentSettings();
};