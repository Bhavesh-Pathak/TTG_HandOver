#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "CyberpunkCityNPCSystem.generated.h"

UENUM(BlueprintType)
enum class ENPCType : uint8
{
    Friendly UMETA(DisplayName = "Friendly"),
    Neutral UMETA(DisplayName = "Neutral"),
    Hostile UMETA(DisplayName = "Hostile")
};

UENUM(BlueprintType)
enum class ENPCBehavior : uint8
{
    Stationary UMETA(DisplayName = "Stationary"),
    Patrol UMETA(DisplayName = "Patrol"),
    Follow UMETA(DisplayName = "Follow"),
    Aggressive UMETA(DisplayName = "Aggressive")
};

USTRUCT(BlueprintType)
struct FCyberpunkCityNPCStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Health = 100;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Attack = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    int32 Defense = 10;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float MovementSpeed = 300.0f;
};

USTRUCT(BlueprintType)
struct FCyberpunkCityNPCData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString NPCID;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString NPCName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString Role;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    ENPCType NPCType = ENPCType::Neutral;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FString Location;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    TArray<FString> Dialogue;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    ENPCBehavior Behavior = ENPCBehavior::Stationary;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    FCyberpunkCityNPCStats Stats;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    TArray<FString> Inventory;
};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API ACyberpunkCityNPC : public ACharacter
{
    GENERATED_BODY()

public:
    ACyberpunkCityNPC();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Data")
    FCyberpunkCityNPCData NPCData;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    class USphereComponent* InteractionSphere;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    int32 CurrentDialogueIndex = 0;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC")
    bool bCanInteract = true;

public:
    virtual void Tick(float DeltaTime) override;

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void InitializeFromData(const FCyberpunkCityNPCData& Data);

    UFUNCTION(BlueprintCallable, Category = "NPC")
    FString GetCurrentDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    FString GetNextDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    bool HasMoreDialogue() const;

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void ResetDialogue();

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void StartInteraction(AActor* InteractingActor);

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void EndInteraction();

    UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
    void OnInteractionStarted(AActor* InteractingActor);

    UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
    void OnInteractionEnded();

    UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
    void OnDialogueChanged(const FString& NewDialogue);

protected:
    UFUNCTION()
    void OnInteractionSphereBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

    UFUNCTION()
    void OnInteractionSphereEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

private:
    void UpdateBehavior();
    void HandlePatrolBehavior();
    void HandleAggressiveBehavior();
};

UCLASS(BlueprintType, Blueprintable)
class GAMEMODULE_API ACyberpunkCityNPCManager : public AActor
{
    GENERATED_BODY()

public:
    ACyberpunkCityNPCManager();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Manager")
    TArray<FCyberpunkCityNPCData> NPCDatabase;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "NPC Manager")
    TSubclassOf<ACyberpunkCityNPC> NPCClass;

    UPROPERTY(BlueprintReadOnly, Category = "NPC Manager")
    TArray<ACyberpunkCityNPC*> SpawnedNPCs;

public:
    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    void LoadNPCsFromJSON();

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    ACyberpunkCityNPC* SpawnNPC(const FString& NPCID, const FVector& Location, const FRotator& Rotation);

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    ACyberpunkCityNPC* FindNPCByID(const FString& NPCID);

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    TArray<ACyberpunkCityNPC*> GetNPCsByType(ENPCType NPCType);

    UFUNCTION(BlueprintCallable, Category = "NPC Manager")
    void SpawnAllNPCs();
};