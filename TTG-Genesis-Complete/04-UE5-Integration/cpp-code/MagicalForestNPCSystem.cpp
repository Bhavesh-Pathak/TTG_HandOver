#include "MagicalForestNPCSystem.h"
#include "Engine/Engine.h"
#include "Components/SphereComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Misc/FileHelper.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonReader.h"

AMagicalForestNPC::AMagicalForestNPC()
{
    PrimaryActorTick.bCanEverTick = true;

    // Create interaction sphere
    InteractionSphere = CreateDefaultSubobject<USphereComponent>(TEXT("InteractionSphere"));
    InteractionSphere->SetupAttachment(RootComponent);
    InteractionSphere->SetSphereRadius(200.0f);
    InteractionSphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    InteractionSphere->SetCollisionResponseToAllChannels(ECR_Ignore);
    InteractionSphere->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);

    // Bind overlap events
    InteractionSphere->OnComponentBeginOverlap.AddDynamic(this, &AMagicalForestNPC::OnInteractionSphereBeginOverlap);
    InteractionSphere->OnComponentEndOverlap.AddDynamic(this, &AMagicalForestNPC::OnInteractionSphereEndOverlap);
}

void AMagicalForestNPC::BeginPlay()
{
    Super::BeginPlay();

    // Apply stats to character
    if (GetCharacterMovement())
    {
        GetCharacterMovement()->MaxWalkSpeed = NPCData.Stats.MovementSpeed;
    }
}

void AMagicalForestNPC::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    UpdateBehavior();
}

void AMagicalForestNPC::InitializeFromData(const FMagicalForestNPCData& Data)
{
    NPCData = Data;

    // Apply movement speed
    if (GetCharacterMovement())
    {
        GetCharacterMovement()->MaxWalkSpeed = NPCData.Stats.MovementSpeed;
    }

    UE_LOG(LogTemp, Warning, TEXT("Initialized NPC: %s"), *NPCData.NPCName);
}

FString AMagicalForestNPC::GetCurrentDialogue()
{
    if (NPCData.Dialogue.IsValidIndex(CurrentDialogueIndex))
    {
        return NPCData.Dialogue[CurrentDialogueIndex];
    }
    return TEXT("...");
}

FString AMagicalForestNPC::GetNextDialogue()
{
    if (HasMoreDialogue())
    {
        CurrentDialogueIndex++;
        FString NewDialogue = GetCurrentDialogue();
        OnDialogueChanged(NewDialogue);
        return NewDialogue;
    }
    return GetCurrentDialogue();
}

bool AMagicalForestNPC::HasMoreDialogue() const
{
    return CurrentDialogueIndex < NPCData.Dialogue.Num() - 1;
}

void AMagicalForestNPC::ResetDialogue()
{
    CurrentDialogueIndex = 0;
}

void AMagicalForestNPC::StartInteraction(AActor* InteractingActor)
{
    if (bCanInteract)
    {
        OnInteractionStarted(InteractingActor);
        UE_LOG(LogTemp, Warning, TEXT("Started interaction with %s"), *NPCData.NPCName);
    }
}

void AMagicalForestNPC::EndInteraction()
{
    OnInteractionEnded();
    ResetDialogue();
}

void AMagicalForestNPC::OnInteractionSphereBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
    // Handle player entering interaction range
    if (OtherActor && OtherActor->IsA<APawn>())
    {
        UE_LOG(LogTemp, Warning, TEXT("Player entered interaction range of %s"), *NPCData.NPCName);
    }
}

void AMagicalForestNPC::OnInteractionSphereEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
    // Handle player leaving interaction range
    if (OtherActor && OtherActor->IsA<APawn>())
    {
        EndInteraction();
        UE_LOG(LogTemp, Warning, TEXT("Player left interaction range of %s"), *NPCData.NPCName);
    }
}

void AMagicalForestNPC::UpdateBehavior()
{
    switch (NPCData.Behavior)
    {
        case ENPCBehavior::Patrol:
            HandlePatrolBehavior();
            break;
        case ENPCBehavior::Aggressive:
            HandleAggressiveBehavior();
            break;
        case ENPCBehavior::Stationary:
        case ENPCBehavior::Follow:
        default:
            // Handled in Blueprint or other systems
            break;
    }
}

void AMagicalForestNPC::HandlePatrolBehavior()
{
    // Basic patrol logic - can be expanded in Blueprint
}

void AMagicalForestNPC::HandleAggressiveBehavior()
{
    // Basic aggressive behavior - can be expanded in Blueprint
}

// NPC Manager Implementation
AMagicalForestNPCManager::AMagicalForestNPCManager()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AMagicalForestNPCManager::BeginPlay()
{
    Super::BeginPlay();

    LoadNPCsFromJSON();
    SpawnAllNPCs();
}

void AMagicalForestNPCManager::LoadNPCsFromJSON()
{
    FString FilePath = FPaths::ProjectContentDir() + TEXT("Data/NPCData.json");
    FString JsonString;

    if (FFileHelper::LoadFileToString(JsonString, *FilePath))
    {
        TSharedPtr<FJsonObject> JsonObject;
        TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonString);

        if (FJsonSerializer::Deserialize(Reader, JsonObject))
        {
            const TArray<TSharedPtr<FJsonValue>>* NPCArray;
            if (JsonObject->TryGetArrayField(TEXT("npcs"), NPCArray))
            {
                for (const TSharedPtr<FJsonValue>& NPCValue : *NPCArray)
                {
                    const TSharedPtr<FJsonObject>& NPCObj = NPCValue->AsObject();

                    FMagicalForestNPCData NewNPC;
                    NewNPC.NPCID = NPCObj->GetStringField(TEXT("id"));
                    NewNPC.NPCName = NPCObj->GetStringField(TEXT("name"));
                    NewNPC.Role = NPCObj->GetStringField(TEXT("role"));
                    NewNPC.Location = NPCObj->GetStringField(TEXT("location"));

                    // Parse NPC type
                    FString TypeString = NPCObj->GetStringField(TEXT("type"));
                    if (TypeString == TEXT("friendly"))
                        NewNPC.NPCType = ENPCType::Friendly;
                    else if (TypeString == TEXT("hostile"))
                        NewNPC.NPCType = ENPCType::Hostile;
                    else
                        NewNPC.NPCType = ENPCType::Neutral;

                    // Parse behavior
                    FString BehaviorString = NPCObj->GetStringField(TEXT("behavior"));
                    if (BehaviorString.Contains(TEXT("patrol")))
                        NewNPC.Behavior = ENPCBehavior::Patrol;
                    else if (BehaviorString.Contains(TEXT("aggressive")))
                        NewNPC.Behavior = ENPCBehavior::Aggressive;
                    else
                        NewNPC.Behavior = ENPCBehavior::Stationary;

                    // Parse dialogue
                    const TArray<TSharedPtr<FJsonValue>>* DialogueArray;
                    if (NPCObj->TryGetArrayField(TEXT("dialogue"), DialogueArray))
                    {
                        for (const TSharedPtr<FJsonValue>& DialogueValue : *DialogueArray)
                        {
                            NewNPC.Dialogue.Add(DialogueValue->AsString());
                        }
                    }

                    // Parse stats
                    const TSharedPtr<FJsonObject>* StatsObj;
                    if (NPCObj->TryGetObjectField(TEXT("stats"), StatsObj))
                    {
                        NewNPC.Stats.Health = (*StatsObj)->GetIntegerField(TEXT("health"));
                        NewNPC.Stats.Attack = (*StatsObj)->GetIntegerField(TEXT("attack"));
                        NewNPC.Stats.Defense = (*StatsObj)->GetIntegerField(TEXT("defense"));
                    }

                    // Parse inventory
                    const TArray<TSharedPtr<FJsonValue>>* InventoryArray;
                    if (NPCObj->TryGetArrayField(TEXT("inventory"), InventoryArray))
                    {
                        for (const TSharedPtr<FJsonValue>& ItemValue : *InventoryArray)
                        {
                            NewNPC.Inventory.Add(ItemValue->AsString());
                        }
                    }

                    NPCDatabase.Add(NewNPC);
                }
            }
        }
    }
}

AMagicalForestNPC* AMagicalForestNPCManager::SpawnNPC(const FString& NPCID, const FVector& Location, const FRotator& Rotation)
{
    if (!NPCClass)
    {
        UE_LOG(LogTemp, Error, TEXT("NPC Class not set in NPCManager"));
        return nullptr;
    }

    // Find NPC data
    FMagicalForestNPCData* NPCData = NPCDatabase.FindByPredicate([&NPCID](const FMagicalForestNPCData& Data)
    {
        return Data.NPCID == NPCID;
    });

    if (!NPCData)
    {
        UE_LOG(LogTemp, Error, TEXT("NPC data not found for ID: %s"), *NPCID);
        return nullptr;
    }

    // Spawn NPC
    AMagicalForestNPC* SpawnedNPC = GetWorld()->SpawnActor<AMagicalForestNPC>(NPCClass, Location, Rotation);
    if (SpawnedNPC)
    {
        SpawnedNPC->InitializeFromData(*NPCData);
        SpawnedNPCs.Add(SpawnedNPC);
        UE_LOG(LogTemp, Warning, TEXT("Spawned NPC: %s"), *NPCData->NPCName);
    }

    return SpawnedNPC;
}

AMagicalForestNPC* AMagicalForestNPCManager::FindNPCByID(const FString& NPCID)
{
    for (AMagicalForestNPC* NPC : SpawnedNPCs)
    {
        if (NPC && NPC->NPCData.NPCID == NPCID)
        {
            return NPC;
        }
    }
    return nullptr;
}

TArray<AMagicalForestNPC*> AMagicalForestNPCManager::GetNPCsByType(ENPCType NPCType)
{
    TArray<AMagicalForestNPC*> FilteredNPCs;

    for (AMagicalForestNPC* NPC : SpawnedNPCs)
    {
        if (NPC && NPC->NPCData.NPCType == NPCType)
        {
            FilteredNPCs.Add(NPC);
        }
    }

    return FilteredNPCs;
}

void AMagicalForestNPCManager::SpawnAllNPCs()
{
    // Spawn NPCs at default locations - can be customized
    for (int32 i = 0; i < NPCDatabase.Num(); i++)
    {
        FVector SpawnLocation = FVector(i * 500.0f, 0.0f, 100.0f); // Spread NPCs out
        SpawnNPC(NPCDatabase[i].NPCID, SpawnLocation, FRotator::ZeroRotator);
    }
}